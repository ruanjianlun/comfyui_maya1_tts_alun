# 🚀 Quick Start Guide

[中文快速开始](QUICKSTART.zh-CN.md) | English

## 1. Installation (3 steps)

### Step 1: Copy folder
Copy `comfyui_alun_maya1` folder to:
```
ComfyUI/custom_nodes/
```

### Step 2: Install dependencies
```bash
cd ComfyUI/custom_nodes/comfyui_alun_maya1
pip install -r requirements.txt
```

### Step 3: Restart ComfyUI
Restart and the node will load automatically!

---

## 2. Usage (3 steps)

### Step 1: Add node
Right-click canvas → `Add Node` → `audio` → `maya1` → `Maya1 Text to Speech`

### Step 2: Configure parameters
- **text**: Enter English text to convert
- **voice_preset**: Select voice style (default: Male-Mature)
- **chunk_length**: Keep default 50
- **temperature**: Keep default 0.4

### Step 3: Generate audio
Click `Queue Prompt` to start generation!

---

## 3. Voice Preset Description

| Preset Name | Best For |
|-------------|----------|
| Male-Mature | Narration, teaching, broadcasting |
| Female-Gentle | Customer service, guidance, warm prompts |
| Male-Energetic | Advertising, promotion, motivation |
| Female-Professional | Business, news, formal occasions |
| Neutral-Broadcast | Standard broadcasting, announcements |

---

## 4. Common Questions

### Q: First run is slow?
A: Normal, needs to download models (~4GB), only once.

### Q: Where are generated audio files?
A: `ComfyUI/output/maya_tts_XXXXXX.wav`

### Q: How to get better results?
A: 
- Use complete, grammatically correct English sentences
- Adjust temperature (0.3-0.5 works well)
- Try different voice presets

---

## 5. Example Text

### Narration (Male-Mature)
```
In the beginning, there was nothing but darkness. 
Then, light emerged, bringing hope to the world.
```

### Dialogue (Female-Gentle)
```
Hello! Welcome to our service. 
How may I assist you today?
```

### Advertisement (Male-Energetic)
```
Don't miss this amazing opportunity! 
Limited time offer, act now!
```

---

## 6. Need More Help?

- 📖 Complete documentation: See `README.md`
- 🔧 Installation issues: See `INSTALL.md`
- 🎨 Workflow guide: See `WORKFLOW_GUIDE.md`
- 📊 Project summary: See `PROJECT_SUMMARY.md`

---

**🎉 Start enjoying high-quality speech synthesis!**
