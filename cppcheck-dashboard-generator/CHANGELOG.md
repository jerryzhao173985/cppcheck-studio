# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-20

### Added
- Initial release of cppcheck-dashboard-generator
- Virtual scrolling support for handling large datasets (100,000+ issues)
- Interactive filtering by severity, file path, and search terms
- Code context display with syntax highlighting
- Comprehensive statistics and visualizations
- Standalone HTML output that works offline
- CLI interface for easy command-line usage
- Programmatic API for integration with other tools
- TypeScript implementation based on proven Python version
- Full test suite with unit and integration tests
- Examples for basic and advanced usage
- Comprehensive documentation

### Features
- Generate beautiful HTML dashboards from cppcheck JSON output
- Handle millions of issues efficiently with smooth performance
- Responsive design that works on desktop and mobile
- Customizable dashboard configuration
- Verbose logging option for debugging
- Support for custom project names and titles

### Technical
- Built with TypeScript for type safety
- Uses JSONL format for efficient data embedding
- Implements virtual DOM for performance
- Minimal dependencies (commander and chalk only)
- Comprehensive test coverage with Jest
- ESLint and Prettier configuration for code quality

## [Unreleased]
- Additional chart types for visualizing trends
- Export functionality for filtered results
- Dark mode theme option
- Real-time file watching and auto-refresh
- Integration with popular CI/CD platforms