# Contributing to cppcheck-dashboard-generator

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/cppcheck-dashboard-generator.git
cd cppcheck-dashboard-generator

# Install dependencies
npm install

# Run tests
npm test

# Run in watch mode during development
npm run dev
```

## Development Workflow

1. **Make your changes**
   ```bash
   # Create a feature branch
   git checkout -b feature/my-new-feature
   ```

2. **Write/update tests**
   - Unit tests go in `test/*.test.ts`
   - Integration tests go in `test/integration.test.ts`

3. **Run tests and linting**
   ```bash
   npm run validate
   ```

4. **Format your code**
   ```bash
   npm run format
   ```

5. **Build and test**
   ```bash
   npm run build
   npm test
   ```

6. **Test CLI locally**
   ```bash
   npm run build
   node dist/cli.js --help
   ```

## Code Style

- We use TypeScript for type safety
- ESLint for linting (configuration in `.eslintrc.js`)
- Prettier for formatting (configuration in `.prettierrc`)
- Follow the existing code style
- Write clear, self-documenting code
- Add JSDoc comments for public APIs

## Testing

- Write unit tests for new functionality
- Maintain or increase code coverage
- Test edge cases and error conditions
- Run `npm test` before submitting PR

## Pull Request Process

1. Update the README.md with details of changes to the interface, if applicable.
2. Update the CHANGELOG.md with your changes under the "Unreleased" section.
3. The PR will be merged once you have the sign-off of at least one maintainer.

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/yourusername/cppcheck-dashboard-generator/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/cppcheck-dashboard-generator/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## References

This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/master/CONTRIBUTING.md)