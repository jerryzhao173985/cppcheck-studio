# cppcheck-dashboard-generator

[![npm version](https://badge.fury.io/js/cppcheck-dashboard-generator.svg)](https://badge.fury.io/js/cppcheck-dashboard-generator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate beautiful, interactive HTML dashboards from cppcheck JSON output with virtual scrolling support for large codebases.

## Features

- 📊 **Interactive Dashboard**: Beautiful, modern UI with real-time filtering and search
- 🚀 **Virtual Scrolling**: Handle millions of issues efficiently with smooth performance
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- 🔍 **Advanced Filtering**: Filter by severity, file path, and search terms
- 📝 **Code Context**: View surrounding code for each issue
- 🎨 **Syntax Highlighting**: Beautiful code display with syntax highlighting
- 📈 **Statistics**: Comprehensive statistics and visualizations
- 💾 **Standalone**: Single HTML file output that works offline

## Installation

```bash
npm install -g cppcheck-dashboard-generator
```

Or use locally in your project:

```bash
npm install cppcheck-dashboard-generator
```

## Usage

### Command Line

```bash
# Basic usage
cppcheck-dashboard input.json output.html

# With options
cppcheck-dashboard input.json output.html --title "My Project Analysis" --project-name "MyProject"

# Show help
cppcheck-dashboard --help
```

### Programmatic API

```typescript
import { StandaloneVirtualDashboardGenerator } from 'cppcheck-dashboard-generator';

const generator = new StandaloneVirtualDashboardGenerator({
  input: 'analysis.json',
  output: 'dashboard.html',
  title: 'Code Analysis Dashboard',
  projectName: 'My Project',
  verbose: true
});

await generator.generate();
```

### Advanced Usage

```typescript
import { 
  StandaloneVirtualDashboardGenerator,
  type GeneratorOptions,
  type DashboardConfig 
} from 'cppcheck-dashboard-generator';

// Custom configuration
const config: Partial<DashboardConfig> = {
  ROW_HEIGHT: 60,
  VISIBLE_BUFFER: 10,
  BATCH_SIZE: 100
};

const options: GeneratorOptions = {
  input: 'analysis.json',
  output: 'custom-dashboard.html',
  title: 'Custom Dashboard',
  projectName: 'My Project',
  config,
  verbose: true
};

const generator = new StandaloneVirtualDashboardGenerator(options);
await generator.generate();
```

## Input Format

The generator expects a JSON file with cppcheck analysis results:

```json
{
  "issues": [
    {
      "file": "src/main.cpp",
      "line": 42,
      "severity": "error",
      "message": "Memory leak: buffer",
      "id": "memleak",
      "code_context": {
        "lines": [
          { "number": 41, "content": "char* buffer = new char[256];" },
          { "number": 42, "content": "return 0;", "is_target": true },
          { "number": 43, "content": "}" }
        ]
      }
    }
  ]
}
```

## Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `input` | string | Path to cppcheck JSON file (required) |
| `output` | string | Path for output HTML file |
| `title` | string | Dashboard title |
| `projectName` | string | Project name to display |
| `verbose` | boolean | Enable verbose logging |
| `config` | object | Custom dashboard configuration |

### Dashboard Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `ROW_HEIGHT` | number | 50 | Height of each row in pixels |
| `VISIBLE_BUFFER` | number | 5 | Extra rows to render outside viewport |
| `SCROLL_DEBOUNCE` | number | 10 | Scroll event debounce in ms |
| `SEARCH_DEBOUNCE` | number | 300 | Search input debounce in ms |
| `BATCH_SIZE` | number | 100 | Items to process per batch |

## Examples

### Generate from cppcheck output

First, run cppcheck with JSON output:

```bash
cppcheck --enable=all --xml --xml-version=2 src/ 2> cppcheck.xml
python -m cppcheck.cppcheck_xml_to_json cppcheck.xml > analysis.json
```

Then generate the dashboard:

```bash
cppcheck-dashboard analysis.json dashboard.html
```

### Integration with CI/CD

```yaml
# GitHub Actions example
- name: Run cppcheck
  run: cppcheck --enable=all --output-file=cppcheck.json --template="{file}:{line}:{severity}:{message}" src/

- name: Generate dashboard
  run: npx cppcheck-dashboard-generator cppcheck.json analysis-dashboard.html

- name: Upload dashboard
  uses: actions/upload-artifact@v3
  with:
    name: cppcheck-dashboard
    path: analysis-dashboard.html
```

## API Reference

### Classes

#### `StandaloneVirtualDashboardGenerator`

Main generator class for creating dashboards.

```typescript
class StandaloneVirtualDashboardGenerator {
  constructor(options: GeneratorOptions);
  generate(): Promise<void>;
  loadAnalysisData(): Promise<AnalysisData>;
  calculateStats(): Stats;
  generateHtml(stats: Stats, issuesJsonl: string, codeJsonl: string, hasContext: boolean): string;
}
```

### Types

See the [TypeScript definitions](./dist/types.d.ts) for complete type information.

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/cppcheck-dashboard-generator.git
cd cppcheck-dashboard-generator

# Install dependencies
npm install

# Run tests
npm test

# Build
npm run build

# Run linting
npm run lint
```

## License

MIT © CPPCheck Dashboard Team

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

This TypeScript implementation is based on the original Python implementation from the CPPCheck Studio project.