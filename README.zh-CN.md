# 🎙️ Maya1 TTS ComfyUI 自定义节点

一个基于 Maya1 模型的高质量文本转语音（Text-to-Speech）ComfyUI 自定义节点，支持多种语音风格和灵活的参数配置。

## ✨ 功能特点

- 🎵 **高质量语音合成**：基于 Maya1 先进的语音生成模型
- 🎨 **多种语音风格**：内置5种语音预设（男性、女性、不同年龄段）
- 🔧 **灵活参数配置**：支持温度、分块长度等参数调整
- 💾 **自动模型管理**：模型自动下载并缓存到 ComfyUI models 目录
- ⚡ **智能缓存**：模型仅加载一次，提高生成效率
- 🌐 **完整中文支持**：界面和日志全中文显示

## 📦 安装

### 方法1：直接克隆到 ComfyUI 自定义节点目录

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/your-repo/comfyui_alun_maya1.git
cd comfyui_alun_maya1
pip install -r requirements.txt
```

### 方法2：手动安装

1. 将整个项目文件夹复制到 `ComfyUI/custom_nodes/` 目录
2. 安装依赖：

```bash
pip install -r requirements.txt
```

### 依赖包

主要依赖包括：
- `transformers` - Hugging Face 模型库
- `torch` - PyTorch 深度学习框架
- `snac` - SNAC 音频编解码器
- `soundfile` - 音频文件处理
- `numpy` - 数值计算

## 🚀 使用方法

### 1. 在 ComfyUI 中添加节点

1. 启动 ComfyUI
2. 右键点击画布，选择 `Add Node` -> `🎵 Audio` -> `Maya1 TTS` -> `🎙️ Maya1 文本转语音`
3. 节点会自动出现在画布上

### 2. 配置节点参数

节点提供以下参数：

| 参数名称 | 类型 | 说明 | 默认值 |
|---------|------|------|--------|
| **text** | 文本 | 要转换为语音的文本内容 | "Hello, this is a test..." |
| **voice_preset** | 下拉选择 | 语音风格预设 | 男性-成熟 |
| **chunk_length** | 整数 | 文本分块长度（字符数） | 50 |
| **temperature** | 浮点数 | 生成温度（0.1-1.0，越高越随机） | 0.4 |
| **custom_description** | 文本（可选） | 自定义语音描述 | 空 |

### 3. 语音风格预设

内置5种语音风格预设：

- **男性-成熟**：30岁左右的男性，美式口音，正常音调，温暖音色
- **女性-温柔**：20岁左右的女性，美式口音，较高音调，柔和音色
- **男性-活力**：20岁左右的男性，美式口音，充满活力，明亮音色
- **女性-专业**：30岁左右的女性，英式口音，专业语调，清晰音色
- **中性-播音**：标准口音，清晰发音，平衡音色，稳定节奏

### 4. 自定义语音描述

如果预设不满足需求，可以使用 `custom_description` 参数自定义语音特征：

```
Realistic male voice in the 40s age with british accent. 
Deep pitch, authoritative tone, slow pacing.
```

描述模板：
- **年龄**：in the 20s/30s/40s age
- **口音**：american/british/australian accent
- **音调**：high/normal/low/deep pitch
- **音色**：warm/bright/soft/clear timbre
- **节奏**：fast/moderate/slow/conversational pacing
- **风格**：energetic/professional/gentle/authoritative tone

## 📁 项目结构

```
comfyui_alun_maya1/
├── __init__.py              # 节点注册入口文件
├── maya_tts_node.py         # 主节点实现文件
├── config.py                # 配置文件（模型路径、常量等）
├── requirements.txt         # Python依赖包列表
├── workflow_example.json    # ComfyUI工作流示例
└── README.md               # 项目说明文档（本文件）
```

## 🔧 配置说明

### 模型存储位置

模型会自动下载到以下位置：
```
ComfyUI/models/maya1_tts_alun/
```

包含以下模型文件：
- Maya1 主模型（约 4GB）
- Maya1 分词器
- SNAC 音频解码器（约 200MB）

### 输出文件位置

生成的音频文件保存在：
```
ComfyUI/output/maya_tts_XXXXXX.wav
```

文件命名格式：`maya_tts_{时间戳}.wav`

### 音频规格

- **采样率**：24000 Hz
- **格式**：WAV（16-bit PCM）
- **声道**：单声道（Mono）

## 📊 工作流示例

项目包含一个基础工作流示例 `workflow_example.json`，演示如何：

1. 使用 Maya1 TTS 节点生成语音
2. 保存生成的音频文件
3. 预览播放音频

### 导入工作流

1. 打开 ComfyUI
2. 点击 `Load` 按钮
3. 选择 `workflow_example.json` 文件
4. 点击 `Queue Prompt` 开始生成

## ⚙️ 高级配置

### 修改默认模型路径

编辑 `config.py` 文件中的 `get_maya_model_path()` 函数：

```python
def get_maya_model_path():
    # 自定义模型路径
    return "/your/custom/path/to/models"
```

### 添加新的语音预设

在 `config.py` 的 `VOICE_PRESETS` 字典中添加：

```python
VOICE_PRESETS = {
    # ... 现有预设
    "自定义预设名": "Your custom voice description here",
}
```

### 清空模型缓存

如需释放显存，可调用：

```python
from config import clear_model_cache
clear_model_cache()
```

## 🐛 常见问题

### Q1: 首次运行很慢怎么办？

**A**: 首次运行需要下载模型（约 4GB），请耐心等待。模型会缓存到本地，后续使用会快很多。

### Q2: 提示显存不足怎么办？

**A**: 
- 减小 `chunk_length` 参数（如改为 30）
- 关闭其他占用显存的程序
- 使用 CPU 模式（自动检测，无需配置）

### Q3: 生成的语音质量不理想？

**A**:
- 调整 `temperature` 参数（0.3-0.5 通常效果较好）
- 尝试不同的语音预设
- 使用自定义描述，更精确地描述想要的语音特征
- 确保输入文本语法正确、标点完整

### Q4: 支持中文吗？

**A**: 当前版本主要支持英文文本转语音，中文支持有限。建议使用英文文本以获得最佳效果。

### Q5: 如何加快生成速度？

**A**:
- 确保使用 GPU（CUDA）
- 减小 `chunk_length`（但可能影响语音连贯性）
- 降低 `temperature` 值
- 将长文本分段处理

## 🔄 更新日志

### v1.0.0 (2025-01-09)

- ✨ 初始版本发布
- 🎵 支持 Maya1 文本转语音
- 🎨 内置 5 种语音预设
- 🔧 灵活的参数配置
- 📁 自动模型管理
- 🌐 完整中文支持

## 📄 许可证

本项目基于 MIT 许可证开源。

## 🙏 致谢

- [Maya Research](https://github.com/maya-research) - Maya1 模型
- [Hugging Face](https://huggingface.co/) - 模型托管
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 工作流平台

## 📮 联系方式

- 作者：Alun
- 问题反馈：请在 GitHub Issues 中提交

## 🌟 支持项目

如果这个项目对你有帮助，欢迎：
- ⭐ Star 本项目
- 🐛 报告 Bug
- 💡 提出新功能建议
- 🤝 贡献代码

---

**享受高质量的语音合成体验！** 🎉
