# 🚀 快速开始指南

## 一、安装（3步完成）

### 步骤1：复制文件夹
将 `comfyui_alun_maya1` 文件夹复制到：
```
ComfyUI/custom_nodes/
```

### 步骤2：安装依赖
```bash
cd ComfyUI/custom_nodes/comfyui_alun_maya1
pip install -r requirements.txt
```

### 步骤3：重启 ComfyUI
重启后节点自动加载！

---

## 二、使用（3步生成）

### 步骤1：添加节点
右键画布 → `Add Node` → `🎵 Audio` → `Maya1 TTS` → `🎙️ Maya1 文本转语音`

### 步骤2：配置参数
- **text**: 输入要转换的英文文本
- **voice_preset**: 选择语音风格（默认：男性-成熟）
- **chunk_length**: 保持默认 50
- **temperature**: 保持默认 0.4

### 步骤3：生成音频
点击 `Queue Prompt` 开始生成！

---

## 三、语音预设说明

| 预设名称 | 适合场景 |
|---------|---------|
| 男性-成熟 | 叙事、教学、播报 |
| 女性-温柔 | 客服、引导、温馨提示 |
| 男性-活力 | 广告、促销、激励 |
| 女性-专业 | 商务、新闻、正式场合 |
| 中性-播音 | 标准播音、公告 |

---

## 四、常见问题

### Q: 首次运行很慢？
A: 正常现象，需下载模型（约4GB），只需一次。

### Q: 在哪里找到生成的音频？
A: `ComfyUI/output/maya_tts_XXXXXX.wav`

### Q: 如何获得更好的效果？
A: 
- 使用完整、语法正确的英文句子
- 调整 temperature (0.3-0.5 效果较好)
- 尝试不同的语音预设

---

## 五、示例文本

### 叙事类（男性-成熟）
```
In the beginning, there was nothing but darkness. 
Then, light emerged, bringing hope to the world.
```

### 对话类（女性-温柔）
```
Hello! Welcome to our service. 
How may I assist you today?
```

### 广告类（男性-活力）
```
Don't miss this amazing opportunity! 
Limited time offer, act now!
```

---

## 六、需要更多帮助？

- 📖 完整文档：查看 `README.md`
- 🔧 安装问题：查看 `INSTALL.md`
- 🎨 工作流：查看 `WORKFLOW_GUIDE.md`
- 📊 项目总结：查看 `PROJECT_SUMMARY.md`

---

**🎉 开始享受高质量的语音合成吧！**
