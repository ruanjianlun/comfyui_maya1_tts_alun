# -*- coding: utf-8 -*-
"""
Maya1 TTS 使用示例
演示如何在独立脚本中使用Maya1 TTS节点
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from maya_tts_node import MayaTTSNode

def main():
    """
    主函数：演示Maya1 TTS的基本使用
    """
    print("=" * 80)
    print("Maya1 TTS 独立使用示例")
    print("=" * 80)
    
    # 创建节点实例
    node = MayaTTSNode()
    
    # 测试文本
    test_texts = [
        {
            "text": "Hello! This is a test of the Maya1 text to speech system.",
            "voice_preset": "男性-成熟",
            "description": "基础测试"
        },
        {
            "text": "Welcome to the future of voice synthesis technology.",
            "voice_preset": "女性-专业",
            "description": "女性专业声音测试"
        },
        {
            "text": "Artificial intelligence is transforming how we interact with computers.",
            "voice_preset": "男性-活力",
            "description": "男性活力声音测试"
        }
    ]
    
    # 遍历测试用例
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n{'=' * 80}")
        print(f"测试用例 {i}/{len(test_texts)}: {test_case['description']}")
        print(f"{'=' * 80}")
        
        try:
            # 生成语音
            result = node.generate_speech(
                text=test_case["text"],
                voice_preset=test_case["voice_preset"],
                chunk_length=50,
                temperature=0.4,
                custom_description=""
            )
            
            # 获取音频数据
            audio_dict = result[0]
            waveform = audio_dict["waveform"]
            sample_rate = audio_dict["sample_rate"]
            
            print(f"✅ 成功生成!")
            print(f"   音频形状: {waveform.shape}")
            print(f"   采样率: {sample_rate} Hz")
            print(f"   时长: {waveform.shape[-1] / sample_rate:.2f} 秒")
            
        except Exception as e:
            print(f"❌ 生成失败: {str(e)}")
    
    print(f"\n{'=' * 80}")
    print("所有测试完成!")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
