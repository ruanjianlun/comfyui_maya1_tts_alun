# -*- coding: utf-8 -*-
"""
Maya1 TTS ComfyUI节点配置文件
用于管理模型路径和缓存
"""
import os
import torch

# 尝试导入ComfyUI的folder_paths模块
try:
    import folder_paths
    HAS_COMFY = True
except ImportError:
    HAS_COMFY = False
    print("Warning: folder_paths module not found, using fallback directory")

# ============================================================================
# 模型路径配置
# ============================================================================

def get_maya_model_path():
    """
    获取Maya1模型存储路径
    优先使用ComfyUI的models目录，否则使用本地目录
    
    Returns:
        str: 模型存储的完整路径
    """
    if HAS_COMFY:
        # ComfyUI环境：使用models/maya1_tts_alun目录
        models_dir = folder_paths.models_dir
        maya_model_dir = os.path.join(models_dir, "maya1_tts_alun")
    else:
        # 独立环境：使用当前目录下的models文件夹
        maya_model_dir = os.path.join(os.path.dirname(__file__), "models", "maya1_tts_alun")
    
    # 确保目录存在
    os.makedirs(maya_model_dir, exist_ok=True)
    return maya_model_dir


def get_output_directory():
    """
    获取音频输出目录
    
    Returns:
        str: 输出目录的完整路径
    """
    if HAS_COMFY:
        return folder_paths.get_output_directory()
    else:
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir


# ============================================================================
# Maya1模型常量
# ============================================================================

# Token ID定义
CODE_START_TOKEN_ID = 128257  # 代码起始标记
CODE_END_TOKEN_ID = 128258    # 代码结束标记
CODE_TOKEN_OFFSET = 128266    # 代码偏移量
SNAC_MIN_ID = 128266          # SNAC最小ID
SNAC_MAX_ID = 156937          # SNAC最大ID
SNAC_TOKENS_PER_FRAME = 7     # 每帧SNAC token数量
SOH_ID = 128259               # 开始头部标记
EOH_ID = 128260               # 结束头部标记
SOA_ID = 128261               # 开始音频标记
BOS_ID = 128000               # 序列起始标记
TEXT_EOT_ID = 128009          # 文本结束标记

# ============================================================================
# 模型缓存
# ============================================================================

# 全局模型缓存字典，避免重复加载模型
MODEL_CACHE = {
    "maya_model": None,       # Maya1主模型
    "maya_tokenizer": None,   # Maya1分词器
    "snac_model": None        # SNAC音频解码器
}


def get_device():
    """
    获取计算设备（CUDA或CPU）
    
    Returns:
        str: "cuda" 或 "cpu"
    """
    return "cuda" if torch.cuda.is_available() else "cpu"


def clear_model_cache():
    """
    清空模型缓存，释放显存
    """
    global MODEL_CACHE
    MODEL_CACHE["maya_model"] = None
    MODEL_CACHE["maya_tokenizer"] = None
    MODEL_CACHE["snac_model"] = None
    
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    print("Model cache cleared")


# ============================================================================
# 默认预设配置
# ============================================================================

# 语音描述预设（不同的声音风格）
VOICE_PRESETS = {
    "Male-Mature": "Realistic male voice in the 30s age with american accent. Normal pitch, warm timbre, conversational pacing.",
    "Female-Gentle": "Realistic female voice in the 20s age with american accent. Slightly high pitch, soft timbre, gentle pacing.",
    "Male-Energetic": "Realistic male voice in the 20s age with american accent. High energy, bright timbre, fast pacing.",
    "Female-Professional": "Realistic female voice in the 30s age with british accent. Professional tone, clear timbre, moderate pacing.",
    "Neutral-Broadcast": "Realistic neutral voice with standard accent. Clear articulation, balanced timbre, steady pacing.",
}

# 生成参数预设
GENERATION_PRESETS = {
    "快速": {
        "max_new_tokens": 1024,
        "temperature": 0.3,
        "top_p": 0.85,
    },
    "标准": {
        "max_new_tokens": 2048,
        "temperature": 0.4,
        "top_p": 0.9,
    },
    "高质量": {
        "max_new_tokens": 3072,
        "temperature": 0.5,
        "top_p": 0.95,
    },
}
