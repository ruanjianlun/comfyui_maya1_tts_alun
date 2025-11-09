# .gitignore 配置说明

本文档说明项目中 `.gitignore` 文件的配置和使用。

## 📋 忽略的文件类型

### 1. Python 相关
```
__pycache__/          # Python 缓存目录
*.py[cod]             # 编译的 Python 文件
*.so                  # C 扩展文件
*.egg-info/           # 包信息
```

### 2. 虚拟环境
```
venv/                 # 标准虚拟环境
comfyui__env/         # 项目虚拟环境
Scripts/              # Windows 虚拟环境脚本
Lib/                  # 虚拟环境库
Include/              # 虚拟环境头文件
pyvenv.cfg            # 虚拟环境配置
```

### 3. IDE 配置
```
.vscode/              # VS Code 配置
.idea/                # PyCharm 配置
*.swp                 # Vim 临时文件
```

### 4. 操作系统文件
```
.DS_Store             # macOS
Thumbs.db             # Windows
desktop.ini           # Windows
```

### 5. 输出文件
```
output/               # 输出目录
output_*.wav          # 测试输出音频
maya_tts_*.wav        # 生成的音频文件
*.mp3, *.flac         # 其他音频格式
```

### 6. 模型文件
```
models/               # 模型目录
*.bin, *.safetensors  # 模型权重文件
*.ckpt, *.pth         # 检查点文件
huggingface/          # HuggingFace 缓存
.cache/               # 通用缓存
```

### 7. 日志和临时文件
```
*.log                 # 日志文件
logs/                 # 日志目录
temp/, tmp/           # 临时目录
*.bak, *.backup       # 备份文件
```

## 🔍 当前项目忽略的文件

根据项目实际情况，以下文件/目录将被忽略：

### 已存在但被忽略
- ✅ `comfyui__env/` - 虚拟环境目录（约 300MB+）
- ✅ `.idea/` - PyCharm IDE 配置
- ✅ `output.wav` - 测试音频文件
- ✅ `output_loop_1.wav` - 测试音频文件

### 运行时生成（将被忽略）
- ✅ `__pycache__/` - Python 缓存
- ✅ `models/maya1_tts_alun/` - 下载的模型（~4GB）
- ✅ `maya_tts_*.wav` - 生成的音频文件
- ✅ `*.log` - 运行日志

## 📝 应该提交的文件

以下是应该提交到 Git 的重要文件：

### Python 代码
```
✅ __init__.py
✅ maya_tts_node.py
✅ config.py
✅ maya_run.py
✅ maya_run_loop.py
✅ test.py
✅ example_usage.py
```

### 配置文件
```
✅ pyproject.toml
✅ requirements.txt
✅ node_list.json
✅ comfyui_node.json
✅ workflow_example.json
```

### 文档文件
```
✅ README.md
✅ README.zh-CN.md
✅ INSTALL.md
✅ INSTALL.zh-CN.md
✅ QUICKSTART.md
✅ QUICKSTART.zh-CN.md
✅ WORKFLOW_GUIDE.md
✅ CHANGELOG.md
✅ CONTRIBUTING.md
✅ LICENSE
✅ .gitignore
... 其他 .md 文档
```

### GitHub 配置
```
✅ .github/workflows/validate.yml
✅ .github/workflows/release.yml
```

## 🚀 使用方法

### 检查哪些文件会被忽略

```bash
# 查看所有被忽略的文件
git status --ignored

# 查看特定文件是否被忽略
git check-ignore -v filename
```

### 查看哪些文件会被提交

```bash
# 查看未跟踪的文件
git status

# 查看所有将被提交的文件
git add --dry-run .
```

### 强制添加被忽略的文件

```bash
# 如果确实需要添加被忽略的文件
git add -f filename
```

## ⚠️ 重要提示

### 不要提交的文件

❌ **虚拟环境** (`comfyui__env/`)
- 太大（300MB+）
- 特定于本地环境
- 通过 `requirements.txt` 重建

❌ **模型文件** (`models/`)
- 非常大（4GB+）
- 会自动下载
- 用户安装时自动获取

❌ **输出文件** (`*.wav`)
- 临时测试文件
- 用户自己生成
- 不属于代码库

❌ **IDE 配置** (`.idea/`, `.vscode/`)
- 个人偏好设置
- 因人而异
- 会导致冲突

❌ **缓存文件** (`__pycache__/`)
- 自动生成
- 特定于 Python 版本
- 每次运行重建

## 🔧 自定义配置

如果需要修改 `.gitignore`：

### 添加忽略规则

```bash
# 在 .gitignore 文件末尾添加
echo "new_pattern/" >> .gitignore
```

### 取消忽略某些文件

```gitignore
# 忽略所有 .wav 文件
*.wav

# 但不忽略 example.wav
!example.wav
```

### 只忽略根目录下的文件

```gitignore
# 只忽略根目录的 output/
/output/

# 忽略所有 output/ 目录
output/
```

## 📊 文件大小参考

| 文件/目录 | 大小 | 是否忽略 |
|-----------|------|----------|
| Python 代码 | < 100KB | ❌ 提交 |
| 文档 | < 500KB | ❌ 提交 |
| `comfyui__env/` | ~300MB | ✅ 忽略 |
| `models/maya1_tts_alun/` | ~4GB | ✅ 忽略 |
| `*.wav` 文件 | 各异 | ✅ 忽略 |
| `.idea/` | ~1MB | ✅ 忽略 |

## ✅ 验证清单

提交前检查：

- [ ] 没有虚拟环境目录
- [ ] 没有 `__pycache__` 目录
- [ ] 没有 `.wav` 音频文件
- [ ] 没有 `models/` 目录
- [ ] 没有 IDE 配置文件
- [ ] 没有个人临时文件
- [ ] 只有源代码和文档
- [ ] `requirements.txt` 是最新的

## 🔍 故障排除

### 问题：文件已被追踪，但想忽略

```bash
# 从 Git 中删除但保留本地文件
git rm --cached filename

# 从 Git 中删除目录但保留本地
git rm -r --cached directory/

# 然后提交
git commit -m "Remove ignored files"
```

### 问题：.gitignore 不生效

```bash
# 清除 Git 缓存
git rm -r --cached .
git add .
git commit -m "Update .gitignore"
```

### 问题：查看特定文件为什么被忽略

```bash
# 查看详细信息
git check-ignore -v filename
```

## 📚 参考资源

- [Git Documentation](https://git-scm.com/docs/gitignore)
- [GitHub .gitignore Templates](https://github.com/github/gitignore)
- [Python .gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore)

---

**配置已优化，可以安全提交代码！** ✅
