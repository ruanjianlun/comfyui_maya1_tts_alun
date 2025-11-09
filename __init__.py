# -*- coding: utf-8 -*-
"""
Maya1 TTS ComfyUI自定义节点包
提供高质量的文本转语音功能

作者: Alun
版本: 1.0.0
"""

# 导入节点类和显示名称映射
from .maya_tts_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 包的公开接口
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 版本信息
__version__ = "1.0.0"
__author__ = "Alun"

# 打印加载信息
print("=" * 60)
print("Maya1 TTS Custom Node Loaded Successfully")
print(f"Version: {__version__}")
print(f"Author: {__author__}")
print(f"Nodes: {len(NODE_CLASS_MAPPINGS)}")
print("=" * 60)
