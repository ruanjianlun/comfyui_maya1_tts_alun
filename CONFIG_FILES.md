# ComfyUI 节点配置文件说明

## 📋 配置文件概述

本项目包含多个配置文件，用于在 ComfyUI 生态系统中正确注册和管理节点。

## 📁 配置文件列表

### 1. `node_list.json` ⭐ 主要配置
**用途**: ComfyUI Manager 节点注册文件

这是最重要的配置文件，用于将节点添加到 ComfyUI Manager 的节点列表中。

**包含信息**:
- 节点基本信息（作者、标题、ID、版本）
- 安装方式（git-clone）
- 依赖包列表
- 模型信息（Maya1、SNAC）
- 节点详细定义（输入、输出、参数）
- 功能特性列表
- 系统要求

**使用方式**:
```bash
# ComfyUI Manager 会自动读取此文件
# 或手动提交到 ComfyUI-Manager 的节点列表仓库
```

---

### 2. `pyproject.toml` 📦 Python 打包配置
**用途**: Python 项目标准配置文件（PEP 518）

**包含信息**:
- 项目元数据（名称、版本、描述）
- 依赖管理
- 构建系统配置
- 开发工具配置（black、pytest）
- 项目链接（GitHub、文档）

**使用方式**:
```bash
# 构建 Python 包
pip install build
python -m build

# 安装为可编辑包
pip install -e .
```

---

### 3. `comfyui_node.json` 🔧 节点元数据
**用途**: 节点的详细元数据配置

**包含信息**:
- ComfyUI 特定配置
- 模型下载信息
- 语音预设详情
- 工作流示例引用

**使用方式**:
```python
# 可在代码中读取此配置
import json
with open('comfyui_node.json') as f:
    config = json.load(f)
```

---

### 4. `LICENSE` 📜 开源许可证
**用途**: MIT 开源许可证

允许自由使用、修改和分发，但需保留版权声明。

---

### 5. `.gitignore` 🚫 Git 忽略文件
**用途**: 指定 Git 不跟踪的文件和目录

**忽略内容**:
- Python 缓存文件 (`__pycache__/`)
- 虚拟环境 (`venv/`, `comfyui__env/`)
- 输出文件 (`*.wav`, `output/`)
- IDE 配置 (`.vscode/`, `.idea/`)
- 系统文件 (`.DS_Store`)

---

## 🚀 提交到 ComfyUI Manager

### 步骤 1: 准备 GitHub 仓库

```bash
# 创建 GitHub 仓库
git init
git add .
git commit -m "Initial commit: Maya1 TTS Node"
git remote add origin https://github.com/your-username/comfyui_alun_maya1.git
git push -u origin main
```

### 步骤 2: 更新配置文件中的 URL

在以下文件中替换 `your-username` 为你的 GitHub 用户名：
- `node_list.json`
- `pyproject.toml`
- `comfyui_node.json`

### 步骤 3: 提交到 ComfyUI-Manager

访问 [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager) 仓库：

1. Fork 该仓库
2. 编辑 `custom-node-list.json`
3. 添加 `node_list.json` 中的配置
4. 提交 Pull Request

**或者直接创建 Issue**:
```
Title: Add Maya1 TTS Node
Content:
Repository: https://github.com/your-username/comfyui_alun_maya1
Node List: [粘贴 node_list.json 内容]
```

---

## 📝 配置文件字段说明

### node_list.json 关键字段

```json
{
  "author": "作者名称",
  "title": "节点标题（在 Manager 中显示）",
  "id": "节点唯一标识符",
  "reference": "GitHub 仓库 URL",
  "install_type": "安装方式（git-clone/copy）",
  "pip": ["Python 依赖包列表"],
  "nodename_pattern": "节点名称匹配模式（正则）",
  "tags": ["搜索标签"],
  "category": "节点分类",
  "models": [
    {
      "name": "模型名称",
      "save_path": "保存路径",
      "url": "下载地址"
    }
  ]
}
```

### pyproject.toml 关键字段

```toml
[project]
name = "包名称（PyPI 格式）"
version = "版本号（SemVer）"
dependencies = ["依赖列表"]

[project.urls]
Homepage = "项目主页"
Repository = "代码仓库"
```

---

## 🔄 版本更新流程

### 1. 更新版本号

同时更新以下文件中的版本号：
- `node_list.json` → `version`
- `pyproject.toml` → `[project] version`
- `comfyui_node.json` → `version`
- `__init__.py` → `__version__`

### 2. 更新 CHANGELOG

记录更新内容：
```markdown
## [1.1.0] - 2025-01-15
### Added
- 新增功能

### Fixed
- 修复问题
```

### 3. 提交更新

```bash
git add .
git commit -m "Release v1.1.0"
git tag v1.1.0
git push origin main --tags
```

---

## 📊 配置文件对比

| 文件 | 用途 | 必需 | 读取者 |
|-----|------|------|--------|
| `node_list.json` | Manager 注册 | ✅ 是 | ComfyUI Manager |
| `pyproject.toml` | Python 打包 | ⚪ 可选 | pip, build tools |
| `comfyui_node.json` | 节点元数据 | ⚪ 可选 | 自定义脚本 |
| `__init__.py` | 节点入口 | ✅ 是 | ComfyUI |
| `LICENSE` | 许可证 | ✅ 推荐 | GitHub, 用户 |
| `.gitignore` | Git 配置 | ✅ 推荐 | Git |

---

## 🛠️ 自定义配置

### 修改安装目录

在 `node_list.json` 和 `comfyui_node.json` 中：
```json
"models": [
  {
    "save_path": "models/your_custom_path"
  }
]
```

同时更新 `config.py` 中的路径：
```python
def get_maya_model_path():
    maya_model_dir = os.path.join(models_dir, "your_custom_path")
    return maya_model_dir
```

### 添加新的依赖

在所有相关文件中添加：
```json
// node_list.json
"pip": ["new-package>=1.0.0"]

// pyproject.toml
dependencies = ["new-package>=1.0.0"]

// requirements.txt
new-package>=1.0.0
```

---

## ✅ 配置检查清单

发布前检查：

- [ ] 所有配置文件中的版本号一致
- [ ] GitHub URL 已更新（替换 `your-username`）
- [ ] LICENSE 文件包含正确的年份和作者
- [ ] `.gitignore` 正确排除了敏感文件
- [ ] `node_list.json` 中的依赖列表完整
- [ ] README.md 中的安装说明准确
- [ ] 工作流示例文件存在且可用

---

## 📚 参考资源

- [ComfyUI Manager 文档](https://github.com/ltdrdata/ComfyUI-Manager)
- [PEP 518 - pyproject.toml](https://peps.python.org/pep-0518/)
- [Python 打包指南](https://packaging.python.org/)
- [SemVer 版本规范](https://semver.org/)

---

**配置完成后，你的节点就可以被 ComfyUI Manager 发现和安装了！** 🎉
