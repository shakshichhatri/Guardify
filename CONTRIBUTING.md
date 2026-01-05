# Contributing to Respect Ranger

Thank you for your interest in contributing to Respect Ranger! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the GitHub Issues
2. If not, create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Include your environment details (Python version, OS, etc.)

### Submitting Changes

1. **Fork the repository**
2. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the code style guidelines
4. **Add tests** for new functionality
5. **Run the test suite** to ensure nothing breaks:
   ```bash
   python test_bot.py
   ```
6. **Commit your changes** with a clear commit message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
7. **Push to your fork** and submit a pull request

## Code Style Guidelines

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Add type hints where appropriate

## Testing Guidelines

- Write unit tests for all new features
- Ensure all existing tests pass
- Aim for high test coverage
- Test edge cases and error conditions

## Areas for Contribution

### High Priority

- **Machine Learning Integration**: Improve detection accuracy with ML models
- **Multi-language Support**: Add detection for non-English content
- **Performance Optimization**: Handle high-volume message processing
- **Dashboard/UI**: Web interface for reviewing forensics data

### Feature Ideas

- Export reports in various formats (PDF, CSV, HTML)
- Integration with moderation actions (warnings, kicks, bans)
- Configurable detection sensitivity per server
- Image and attachment analysis
- Real-time alerts to moderators
- User reputation system
- Appeal system for false positives

### Documentation

- Improve setup guides
- Add video tutorials
- Create FAQ section
- Translate documentation to other languages
- Add more code examples

## Questions?

If you have questions about contributing, feel free to:
- Open a GitHub Discussion
- Comment on an existing issue
- Reach out to the maintainers

## Code of Conduct

This project aims to create a safe and inclusive environment. By contributing, you agree to:
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other contributors

Thank you for helping make Discord communities safer! 🛡️
