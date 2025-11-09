# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Chinese text support
- More voice presets
- Audio post-processing options
- Batch processing node
- Voice cloning features

## [1.0.0] - 2025-01-09

### Added
- Initial release of Maya1 TTS ComfyUI node
- High-quality text-to-speech using Maya1 model
- 5 built-in voice presets:
  - 男性-成熟 (Mature Male)
  - 女性-温柔 (Gentle Female)
  - 男性-活力 (Energetic Male)
  - 女性-专业 (Professional Female)
  - 中性-播音 (Neutral Broadcasting)
- Customizable voice descriptions
- Adjustable temperature parameter (0.1-1.0)
- Configurable chunk length (20-200 characters)
- Automatic model caching for efficiency
- GPU acceleration support
- 24kHz audio output
- Comprehensive documentation:
  - README.md - Full documentation
  - INSTALL.md - Installation guide
  - WORKFLOW_GUIDE.md - Workflow usage guide
  - QUICKSTART.md - Quick start guide
  - PROJECT_SUMMARY.md - Technical summary
  - CONFIG_FILES.md - Configuration files documentation
- Example workflow (workflow_example.json)
- Standalone usage example (example_usage.py)

### Technical Features
- Model path management using ComfyUI models directory
- Intelligent path selection for ComfyUI/standalone environments
- Complete Chinese code comments for developers
- English UI and console output for international users
- Modular design with config.py for easy maintenance
- Error handling and user-friendly messages

### Models
- Maya1 main model (~4GB) from maya-research/maya1
- SNAC audio decoder (~200MB) from hubertsiuzdak/snac_24khz
- Automatic download to ComfyUI/models/maya1_tts_alun/

### Requirements
- Python >= 3.9
- PyTorch >= 2.0.0
- Transformers >= 4.36.0
- SNAC audio codec
- SoundFile >= 0.12.0
- NumPy >= 1.24.0
- GPU with 4GB+ VRAM (recommended)

### Documentation
- Comprehensive README with installation, usage, and FAQ
- Quick installation guide (3 steps)
- Detailed workflow guide with best practices
- Application scenarios and tips
- Project structure documentation
- Configuration files explained

---

## Version History

### Version Numbering
- **Major version** (1.x.x): Breaking changes or major features
- **Minor version** (x.1.x): New features, backward compatible
- **Patch version** (x.x.1): Bug fixes and minor improvements

### Release Notes Format
Each release includes:
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## Support

For issues and questions:
- GitHub Issues: https://github.com/your-username/comfyui_alun_maya1/issues
- Discussions: https://github.com/your-username/comfyui_alun_maya1/discussions

---

**Note**: Replace `your-username` with your actual GitHub username before publishing.
