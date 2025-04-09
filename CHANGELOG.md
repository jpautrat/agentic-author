# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-04-30

### Added
- Multiple AI provider support (OpenAI, Anthropic Claude, Local LLMs)
- Customizable book parameters (chapter length, scenes, chapter count)
- Local LM Studio integration for API-free generation
- Resilient API handling with automatic retries
- Improved prompting for better style adherence
- Automatic chapter extension for consistent length
- Complete book compilation with title page and table of contents

### Changed
- Enhanced error handling and recovery mechanisms
- Improved configuration system with environment variables
- Better documentation and setup instructions
- Updated requirements and dependencies

### Fixed
- Character encoding issues on Windows
- API overload handling for Anthropic Claude
- Token limit management for different models
- Chapter generation reliability

## [0.1.0] - 2023 (Original Version by Adam Larson)

### Initial Features
- Multi-agent collaborative writing system
- Structured chapter generation
- Story continuity and character development
- Automated world-building
- Support for multi-chapter narratives
