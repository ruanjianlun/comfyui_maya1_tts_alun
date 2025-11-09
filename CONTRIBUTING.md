# Contributing to Maya1 TTS ComfyUI Node

Thank you for your interest in contributing to this project! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## 📜 Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports:
1. Check the [existing issues](https://github.com/your-username/comfyui_alun_maya1/issues)
2. Try the latest version
3. Check the [FAQ](README.md#常见问题) in README.md

When reporting bugs, include:
- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, GPU info
- **Logs**: Console output and error messages

### Suggesting Features

Feature requests are welcome! Please include:
- **Use Case**: Why is this feature needed?
- **Description**: What should it do?
- **Examples**: How would it work?
- **Alternatives**: Other solutions you've considered

### Code Contributions

Contributions can include:
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Test coverage
- 🌐 Translations

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/your-username/comfyui_alun_maya1.git
cd comfyui_alun_maya1
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## 📐 Coding Standards

### Python Style

Follow PEP 8 with these guidelines:
- Line length: 100 characters (120 max)
- Use 4 spaces for indentation
- Use descriptive variable names
- Add type hints where applicable

### Code Formatting

```bash
# Format code with black
black --line-length=100 *.py

# Check style with flake8
flake8 --max-line-length=120 *.py
```

### Comments and Documentation

- **Chinese comments** for code logic (中文注释便于理解)
- **English docstrings** for public APIs
- **Clear function/class descriptions**

Example:
```python
def generate_audio_chunk(model, tokenizer, text: str) -> np.ndarray:
    """
    Generate audio for a single text chunk.
    
    Args:
        model: Maya1 model instance
        tokenizer: Tokenizer instance
        text: Text to convert to speech
        
    Returns:
        np.ndarray: Generated audio waveform
    """
    # 构建提示词
    prompt = build_prompt(tokenizer, text)
    # ... rest of the code
```

### File Structure

```python
# 1. Imports (standard library, third-party, local)
import os
import torch
from .config import MODEL_CACHE

# 2. Constants
SAMPLE_RATE = 24000

# 3. Helper functions
def helper_function():
    pass

# 4. Main classes
class NodeClass:
    pass

# 5. Exports
__all__ = ['NodeClass']
```

## 🔄 Pull Request Process

### 1. Before Submitting

- [ ] Code follows the style guidelines
- [ ] Comments are clear and helpful
- [ ] Documentation is updated
- [ ] No breaking changes (or documented)
- [ ] Tested locally

### 2. PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (specify)

## Testing
How did you test this?

## Screenshots (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No warnings/errors
- [ ] Tested in ComfyUI
```

### 3. Review Process

1. Submit PR with clear description
2. Wait for maintainer review
3. Address feedback if any
4. Once approved, changes will be merged

### 4. After Merge

- Your contribution will be credited in CHANGELOG
- Close related issues if applicable
- Delete your feature branch

## 🐛 Reporting Bugs

Use this template:

```markdown
**Bug Description**
A clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 11]
- Python: [e.g., 3.10.0]
- PyTorch: [e.g., 2.0.0]
- GPU: [e.g., NVIDIA RTX 3090]
- VRAM: [e.g., 24GB]

**Additional Context**
Any other information
```

## ✨ Suggesting Features

Use this template:

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this needed?

**Proposed Solution**
How should it work?

**Alternatives**
Other solutions considered

**Additional Context**
Any other information
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_node.py

# Run with coverage
pytest --cov=. tests/
```

### Test Guidelines

- Write tests for new features
- Update tests when changing behavior
- Test both success and failure cases
- Include edge cases

## 📝 Documentation

### What to Document

- New features and parameters
- Breaking changes
- Migration guides
- Examples and use cases

### Where to Update

- `README.md` - Main documentation
- `WORKFLOW_GUIDE.md` - Usage examples
- Code comments - Implementation details
- `CHANGELOG.md` - Version history

## 🌐 Internationalization

### Adding Translations

Help translate documentation:
1. Copy existing .md file
2. Translate to target language
3. Name it with language code (e.g., README.zh-CN.md)
4. Submit PR

## 💬 Communication

- **GitHub Issues**: Bug reports and features
- **GitHub Discussions**: Questions and ideas
- **Pull Requests**: Code contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in CHANGELOG.md
- Mentioned in release notes
- Credited in README.md (for significant contributions)

## ❓ Questions?

Feel free to:
- Open a discussion on GitHub
- Ask in pull request comments
- Create an issue with the question label

---

Thank you for contributing to make this project better! 🚀
