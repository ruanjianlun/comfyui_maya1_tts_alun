# Maya1 TTS ComfyUI Node Installation Guide

[中文安装指南](INSTALL.zh-CN.md) | English

## Quick Installation

### Step 1: Copy Files

Copy the entire `comfyui_alun_maya1` folder to the ComfyUI custom nodes directory:

```
ComfyUI/custom_nodes/comfyui_alun_maya1/
```

### Step 2: Install Dependencies

Open command line, navigate to the node directory and install dependencies:

```bash
cd ComfyUI/custom_nodes/comfyui_alun_maya1
pip install -r requirements.txt
```

Or install in ComfyUI's virtual environment:

```bash
# Windows
ComfyUI\venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
source ComfyUI/venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Restart ComfyUI

Restart ComfyUI and the node will load automatically.

## Verify Installation

1. Launch ComfyUI
2. Right-click on the canvas
3. Look for menu: `Add Node` -> `audio` -> `maya1`
4. If you see the `Maya1 Text to Speech` node, installation was successful!

## First Use

On first use, the node will automatically download model files (~4GB), this may take a few minutes.

Models will be saved to:
```
ComfyUI/models/maya1_tts_alun/
```

## Potential Issues

### Issue 1: Node not found

**Solution**:
- Confirm folder name is `comfyui_alun_maya1`
- Confirm `__init__.py` file exists
- Check ComfyUI startup logs for error messages

### Issue 2: Dependency installation failed

**Solution**:
```bash
# Install packages individually
pip install transformers
pip install torch
pip install snac
pip install soundfile
pip install numpy
```

### Issue 3: CUDA-related errors

**Solution**:
- Ensure you have a CUDA-compatible PyTorch version installed
- Visit https://pytorch.org/ to select the appropriate installation command

## Need Help?

Check the complete documentation: `README.md`
