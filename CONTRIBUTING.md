# Contributing to Gynecology Chatbot

Thank you for your interest in contributing to the Gynecology Chatbot project! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in the issues
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features
1. Check if the feature has already been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Pull Requests
1. Fork the repository
2. Create a new branch for your feature/fix
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 💻 Development Setup

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/gynecology_chatbot.git
cd gynecology_chatbot

# Set up backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate

# Set up frontend
cd ../chainlit_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
cd ..
chmod +x test_system.sh
./test_system.sh
```

## 📋 Coding Standards

### Python Code
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### Django Specific
- Follow Django best practices
- Use Django's built-in features when possible
- Properly handle database migrations
- Use Django's security features

### Frontend
- Use modern JavaScript/React patterns
- Keep components small and reusable
- Follow accessibility guidelines
- Test UI components thoroughly

## 🧪 Testing

### Running Tests
```bash
# Run system tests
./test_system.sh

# Test individual components
cd backend
python3 manage.py test

# Test API endpoints
curl http://localhost:9000/api/health/
```

### Writing Tests
- Write unit tests for new functions
- Add integration tests for new features
- Test error cases and edge conditions
- Update test documentation

## 📝 Documentation

### Code Documentation
- Add docstrings to all public functions
- Comment complex logic
- Update README.md for new features
- Include examples in documentation

### API Documentation
- Document new API endpoints
- Include request/response examples
- Update Postman collections if available

## 🔒 Security Guidelines

### API Keys
- Never commit API keys to version control
- Use environment variables for sensitive data
- Validate all user inputs
- Follow security best practices

### Medical Information
- Ensure medical information is accurate
- Add disclaimers where appropriate
- Follow medical software guidelines
- Respect user privacy

## 📋 Pull Request Process

1. **Before Submitting**
   - Ensure your code passes all tests
   - Update documentation if needed
   - Follow the coding standards
   - Test your changes thoroughly

2. **PR Description**
   - Clear title describing the change
   - Detailed description of what was changed
   - Link to related issues
   - Screenshots for UI changes

3. **Review Process**
   - Maintainers will review your PR
   - Address any requested changes
   - PR will be merged once approved

## 🏷️ Git Workflow

### Branch Naming
- `feature/description` for new features
- `bugfix/description` for bug fixes
- `docs/description` for documentation updates
- `refactor/description` for code refactoring

### Commit Messages
```
type(scope): short description

Longer description if needed

Fixes #issue_number
```

Types: feat, fix, docs, style, refactor, test, chore

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- Additional LLM integrations
- Improved error handling
- Performance optimizations
- Security enhancements
- Test coverage improvements

### Medium Priority
- UI/UX improvements
- Additional appointment features
- Database optimizations
- Documentation improvements

### Low Priority
- Code refactoring
- Additional themes
- Extra configuration options

## 🆘 Getting Help

If you need help with development:

1. Check the documentation
2. Look at existing code examples
3. Ask questions in issues
4. Contact the maintainers

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🙏 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to women's health technology! 💜
