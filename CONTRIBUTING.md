# Contributing to CPPCheck Studio

Thank you for your interest in contributing to CPPCheck Studio!

## Code Style

### Python
- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Handle errors gracefully with helpful messages

### TypeScript
- Use strict TypeScript configuration
- Document all public APIs with JSDoc
- Follow the existing code style

## Testing

Before submitting changes:
1. Test with small and large analysis files
2. Verify dashboards render correctly
3. Check that virtual scrolling works for 5000+ issues
4. Ensure code context extraction handles edge cases

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request with a detailed description

## Development Setup

```bash
# Python development
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# TypeScript development
cd cppcheck-dashboard-generator
npm install
npm run dev
```

## Areas for Improvement

- Add more dashboard themes
- Support for additional static analysis tools
- Integration with CI/CD pipelines
- Performance optimizations for very large datasets
- More sophisticated filtering options

## Questions?

Feel free to open an issue for discussion before starting major changes.