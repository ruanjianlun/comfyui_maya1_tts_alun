# -*- coding: utf-8 -*-
"""
Maya1 TTS ComfyUI Custom Node
High-quality text-to-speech functionality powered by Maya1 model

Author: Alun
Version: 1.0.0
Repository: https://github.com/ruanjianlun/comfyui_maya1_tts_alun
"""

from .maya_tts_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Required exports for ComfyUI Custom Node Manager
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Metadata for ComfyUI Custom Node Manager
__version__ = "1.0.0"
__author__ = "Alun"
__title__ = "Maya1 TTS"
__description__ = "High-quality text-to-speech node using Maya1 model with multiple voice styles"
__web__ = "https://github.com/ruanjianlun/comfyui_maya1_tts_alun"

# Display info when node is loaded
print("\n" + "=" * 70)
print("  🎙️  Maya1 TTS Custom Node Loaded Successfully")
print("=" * 70)
print(f"  Version:     {__version__}")
print(f"  Author:      {__author__}")
print(f"  Nodes:       {len(NODE_CLASS_MAPPINGS)} registered")
print(f"  Repository:  {__web__}")
print("=" * 70 + "\n")
