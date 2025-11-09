# -*- coding: utf-8 -*-
"""
Maya1 TTS ComfyUI节点 - Text to Audio
实现文本转语音功能，支持多种声音风格
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from snac import SNAC
import soundfile as sf
import numpy as np
import re
import os

# 导入配置文件
from .config import (
    get_maya_model_path, 
    get_output_directory,
    CODE_START_TOKEN_ID,
    CODE_END_TOKEN_ID,
    CODE_TOKEN_OFFSET,
    SNAC_MIN_ID,
    SNAC_MAX_ID,
    SNAC_TOKENS_PER_FRAME,
    SOH_ID,
    EOH_ID,
    SOA_ID,
    BOS_ID,
    TEXT_EOT_ID,
    MODEL_CACHE,
    get_device,
    VOICE_PRESETS
)

# 全局模型缓存（使用config中的）
_model_cache = MODEL_CACHE


def split_text(text: str, max_length: int = 50) -> list:
    """
    将文本分割成多个片段，同时保留情感标签
    
    Args:
        text: 要分割的文本
        max_length: 每个片段的最大长度
        
    Returns:
        list: 分割后的文本片段列表
    """
    if len(text) <= max_length:
        return [text]

    # 按句子边界分割（保留标点符号）
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def build_prompt(tokenizer, description: str, text: str) -> str:
    """
    构建Maya1模型的格式化提示词
    
    Args:
        tokenizer: 分词器
        description: 语音描述（音色、风格等）
        text: 要转换的文本内容
        
    Returns:
        str: 格式化后的提示词
    """
    # 解码各种特殊标记
    soh_token = tokenizer.decode([SOH_ID])  # 开始头部
    eoh_token = tokenizer.decode([EOH_ID])  # 结束头部
    soa_token = tokenizer.decode([SOA_ID])  # 开始音频
    sos_token = tokenizer.decode([CODE_START_TOKEN_ID])  # 代码开始
    eot_token = tokenizer.decode([TEXT_EOT_ID])  # 文本结束
    bos_token = tokenizer.bos_token  # 序列开始

    # 构建格式化文本
    formatted_text = f'<description="{description}"> {text}'
    
    # 组装完整提示词
    prompt = (
        soh_token + bos_token + formatted_text + eot_token +
        eoh_token + soa_token + sos_token
    )
    return prompt


def extract_snac_codes(token_ids: list) -> list:
    """
    从生成的token中提取SNAC编码
    
    Args:
        token_ids: 生成的token ID列表
        
    Returns:
        list: 提取的SNAC编码列表
    """
    # 查找结束标记的位置
    try:
        eos_idx = token_ids.index(CODE_END_TOKEN_ID)
    except ValueError:
        eos_idx = len(token_ids)

    # 筛选SNAC范围内的token
    snac_codes = [
        token_id for token_id in token_ids[:eos_idx]
        if SNAC_MIN_ID <= token_id <= SNAC_MAX_ID
    ]
    return snac_codes


def unpack_snac_from_7(snac_tokens: list) -> list:
    """
    将7个token的SNAC帧解包为3个层次级别
    SNAC使用分层量化：每帧7个token -> 3个层次（粗->细）
    
    Args:
        snac_tokens: SNAC token列表
        
    Returns:
        list: [level1, level2, level3]，三个层次的编码列表
    """
    # 移除末尾的结束标记
    if snac_tokens and snac_tokens[-1] == CODE_END_TOKEN_ID:
        snac_tokens = snac_tokens[:-1]

    # 计算完整的帧数
    frames = len(snac_tokens) // SNAC_TOKENS_PER_FRAME
    snac_tokens = snac_tokens[:frames * SNAC_TOKENS_PER_FRAME]

    if frames == 0:
        return [[], [], []]

    # 三个层次的编码列表
    l1, l2, l3 = [], [], []

    # 解包每一帧的7个token到3个层次
    for i in range(frames):
        slots = snac_tokens[i * 7:(i + 1) * 7]
        # Level 1: 1个token（最粗粒度）
        l1.append((slots[0] - CODE_TOKEN_OFFSET) % 4096)
        # Level 2: 2个token（中等粒度）
        l2.extend([
            (slots[1] - CODE_TOKEN_OFFSET) % 4096,
            (slots[4] - CODE_TOKEN_OFFSET) % 4096,
        ])
        # Level 3: 4个token（最细粒度）
        l3.extend([
            (slots[2] - CODE_TOKEN_OFFSET) % 4096,
            (slots[3] - CODE_TOKEN_OFFSET) % 4096,
            (slots[5] - CODE_TOKEN_OFFSET) % 4096,
            (slots[6] - CODE_TOKEN_OFFSET) % 4096,
        ])

    return [l1, l2, l3]


def generate_audio_chunk(model, tokenizer, snac_model, description: str, text: str, device: str, 
                        temperature: float = 0.4, max_new_tokens: int = 2048) -> np.ndarray:
    """
    为单个文本片段生成音频
    
    Args:
        model: Maya1主模型
        tokenizer: 分词器
        snac_model: SNAC音频解码器
        description: 语音描述
        text: 文本内容
        device: 计算设备
        temperature: 采样温度（控制随机性，越高越随机）
        max_new_tokens: 最大生成token数
        
    Returns:
        np.ndarray: 生成的音频数组
    """
    # 构建提示词
    prompt = build_prompt(tokenizer, description, text)

    # 分词并转换为张量
    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    # 使用推理模式生成token
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,  # 最大生成长度
            min_new_tokens=28,               # 最小生成长度
            temperature=temperature,         # 控制随机性
            top_p=0.9,                       # 核采样参数
            repetition_penalty=1.1,          # 重复惩罚
            do_sample=True,                  # 启用采样
            eos_token_id=CODE_END_TOKEN_ID,  # 结束标记
            pad_token_id=tokenizer.pad_token_id,
        )

    # 提取生成的token ID
    generated_ids = outputs[0, inputs['input_ids'].shape[1]:].tolist()
    snac_tokens = extract_snac_codes(generated_ids)

    # 检查是否有足够的token
    if len(snac_tokens) < 7:
        return np.array([])

    # 解包SNAC编码
    levels = unpack_snac_from_7(snac_tokens)
    codes_tensor = [
        torch.tensor(level, dtype=torch.long, device=device).unsqueeze(0)
        for level in levels
    ]

    # 使用SNAC解码器生成音频
    with torch.inference_mode():
        z_q = snac_model.quantizer.from_codes(codes_tensor)
        audio = snac_model.decoder(z_q)[0, 0].cpu().numpy()

    # 移除预热样本（前2048个样本）
    if len(audio) > 2048:
        audio = audio[2048:]

    return audio


class MayaTTSNode:
    """
    ComfyUI节点：Maya1文本转语音
    将文本转换为高质量的语音音频
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入参数类型
        """
        return {
            "required": {
                # 要转换的文本内容
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello, this is a test of Maya1 text to speech system."
                }),
                # 语音风格预设选择
                "voice_preset": (list(VOICE_PRESETS.keys()), {
                    "default": "男性-成熟"
                }),
                # 文本分块长度（字符数）
                "chunk_length": ("INT", {
                    "default": 50,
                    "min": 20,
                    "max": 200,
                    "step": 10,
                    "display": "slider"
                }),
                # 生成温度（控制随机性）
                "temperature": ("FLOAT", {
                    "default": 0.4,
                    "min": 0.1,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider"
                }),
            },
            "optional": {
                # 自定义语音描述（高级选项）
                "custom_description": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            }
        }

    # 节点返回类型：音频
    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    
    # 执行函数名
    FUNCTION = "generate_speech"
    
    # 节点分类
    CATEGORY = "audio/maya1"
    
    # 标记为输出节点
    OUTPUT_NODE = True

    def generate_speech(self, text, voice_preset, chunk_length, temperature, custom_description=""):
        """
        执行文本转语音的主函数
        
        Args:
            text: 要转换的文本
            voice_preset: 语音风格预设
            chunk_length: 文本分块长度
            temperature: 生成温度
            custom_description: 自定义语音描述（可选）
            
        Returns:
            tuple: (音频字典,)
        """
        global _model_cache

        print("\n" + "="*80)
        print("Maya1 TTS - Starting Speech Generation")
        print("="*80)

        # 获取模型路径
        model_path = get_maya_model_path()
        print(f"Model Directory: {model_path}")

        # 加载模型（使用缓存，避免重复加载）
        if _model_cache["maya_model"] is None:
            print("\n[1/3] Loading Maya1 Main Model...")
            _model_cache["maya_model"] = AutoModelForCausalLM.from_pretrained(
                "maya-research/maya1",
                torch_dtype=torch.bfloat16,
                device_map="auto",
                trust_remote_code=True,
                cache_dir=model_path  # 使用ComfyUI的models目录
            )
            _model_cache["maya_tokenizer"] = AutoTokenizer.from_pretrained(
                "maya-research/maya1",
                trust_remote_code=True,
                cache_dir=model_path
            )
            print("✓ Maya1 Model Loaded")

        if _model_cache["snac_model"] is None:
            print("\n[2/3] Loading SNAC Audio Decoder...")
            _model_cache["snac_model"] = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval()
            device = get_device()
            if torch.cuda.is_available():
                _model_cache["snac_model"] = _model_cache["snac_model"].to("cuda")
            print("✓ SNAC Decoder Loaded")

        # 获取缓存的模型
        model = _model_cache["maya_model"]
        tokenizer = _model_cache["maya_tokenizer"]
        snac_model = _model_cache["snac_model"]
        device = get_device()

        # 确定语音描述（优先使用自定义描述）
        if custom_description.strip():
            description = custom_description
            print(f"\nUsing Custom Voice Description")
        else:
            description = VOICE_PRESETS[voice_preset]
            print(f"\nVoice Preset: {voice_preset}")
        
        print(f"Description: {description[:80]}...")

        # 分割文本
        print(f"\n[3/3] Processing Text ({len(text)} characters)...")
        text_chunks = split_text(text, max_length=chunk_length)
        print(f"Split into {len(text_chunks)} chunks")

        # 生成音频片段
        audio_chunks = []
        for i, chunk in enumerate(text_chunks, 1):
            print(f"\nGenerating Chunk {i}/{len(text_chunks)}")
            print(f"Text: {chunk[:60]}...")
            
            audio = generate_audio_chunk(
                model, tokenizer, snac_model, 
                description, chunk, device,
                temperature=temperature
            )
            
            if len(audio) > 0:
                audio_chunks.append(audio)
                duration = len(audio) / 24000
                print(f"✓ Generated {duration:.2f}s audio")
            else:
                print(f"✗ Generation failed (skipped)")

        # 检查是否有生成的音频
        if not audio_chunks:
            raise ValueError("No audio generated. Please check input text.")

        # 合并所有音频片段
        merged_audio = np.concatenate(audio_chunks)
        total_duration = len(merged_audio) / 24000

        # 获取输出目录并保存文件
        output_dir = get_output_directory()
        
        # 生成唯一的文件名（使用时间戳）
        import time
        timestamp = int(time.time() * 1000) % 1000000
        output_file = os.path.join(output_dir, f"maya_tts_{timestamp}.wav")
        sf.write(output_file, merged_audio, 24000)

        print(f"\n" + "="*80)
        print(f"Audio Generation Completed!")
        print(f"File: {os.path.basename(output_file)}")
        print(f"Duration: {total_duration:.2f}s")
        print(f"Sample Rate: 24000 Hz")
        print("="*80 + "\n")

        # 返回ComfyUI标准音频格式
        # waveform: [batch, channels, samples]
        audio_dict = {
            "waveform": torch.from_numpy(merged_audio).unsqueeze(0).unsqueeze(0),
            "sample_rate": 24000
        }

        return (audio_dict,)


# ============================================================================
# ComfyUI节点注册
# ============================================================================

# 节点类映射（内部类名 -> 实际类）
NODE_CLASS_MAPPINGS = {
    "MayaTTSNode": MayaTTSNode
}

# 节点显示名称映射（在ComfyUI界面显示的名称）
NODE_DISPLAY_NAME_MAPPINGS = {
    "MayaTTSNode": "Maya1 Text to Speech"
}
