# Maya1 TTS ComfyUI 节点安装指南

## 快速安装

### 步骤 1: 复制文件

将整个 `comfyui_alun_maya1` 文件夹复制到 ComfyUI 的自定义节点目录：

```
ComfyUI/custom_nodes/comfyui_alun_maya1/
```

### 步骤 2: 安装依赖

打开命令行，进入节点目录并安装依赖：

```bash
cd ComfyUI/custom_nodes/comfyui_alun_maya1
pip install -r requirements.txt
```

或者在 ComfyUI 的虚拟环境中安装：

```bash
# Windows
ComfyUI\venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
source ComfyUI/venv/bin/activate
pip install -r requirements.txt
```

### 步骤 3: 重启 ComfyUI

重启 ComfyUI，节点会自动加载。

## 验证安装

1. 启动 ComfyUI
2. 右键点击画布
3. 查找菜单：`Add Node` -> `🎵 Audio` -> `Maya1 TTS`
4. 如果看到 `🎙️ Maya1 文本转语音` 节点，说明安装成功！

## 首次使用

首次使用时，节点会自动下载模型文件（约 4GB），需要等待几分钟。

模型会保存在：
```
ComfyUI/models/maya1_tts_alun/
```

## 可能的问题

### 问题1: 找不到节点

**解决方案**：
- 确认文件夹名称为 `comfyui_alun_maya1`
- 确认 `__init__.py` 文件存在
- 查看 ComfyUI 启动日志是否有错误信息

### 问题2: 依赖包安装失败

**解决方案**：
```bash
# 单独安装每个包
pip install transformers
pip install torch
pip install snac
pip install soundfile
pip install numpy
```

### 问题3: CUDA 相关错误

**解决方案**：
- 确保已安装支持 CUDA 的 PyTorch 版本
- 访问 https://pytorch.org/ 选择合适的安装命令

## 需要帮助？

查看完整文档：`README.md`
