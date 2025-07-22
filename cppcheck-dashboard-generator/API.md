# API Documentation

## Table of Contents
- [Classes](#classes)
  - [StandaloneVirtualDashboardGenerator](#standalonevirtualdashboardgenerator)
- [Types](#types)
  - [GeneratorOptions](#generatoroptions)
  - [DashboardConfig](#dashboardconfig)
  - [AnalysisData](#analysisdata)
  - [Issue](#issue)
  - [CodeContext](#codecontext)
  - [Stats](#stats)
  - [Severity](#severity)
- [Functions](#functions)
  - [generateStyles](#generatestyles)
  - [generateScripts](#generatescripts)

## Classes

### StandaloneVirtualDashboardGenerator

The main class for generating interactive HTML dashboards from cppcheck JSON output.

#### Constructor

```typescript
constructor(options: GeneratorOptions)
```

Creates a new instance of the dashboard generator.

**Parameters:**
- `options`: Configuration options for the generator

**Example:**
```typescript
const generator = new StandaloneVirtualDashboardGenerator({
  input: 'analysis.json',
  output: 'dashboard.html',
  title: 'My Project Analysis'
});
```

#### Methods

##### generate()

```typescript
async generate(): Promise<void>
```

Generates the HTML dashboard from the input JSON file.

**Throws:**
- `Error` if input file doesn't exist
- `Error` if JSON parsing fails
- `Error` if file writing fails

**Example:**
```typescript
try {
  await generator.generate();
  console.log('Dashboard generated successfully');
} catch (error) {
  console.error('Generation failed:', error);
}
```

##### loadAnalysisData()

```typescript
protected async loadAnalysisData(): Promise<AnalysisData>
```

Loads and parses the analysis data from the input file.

**Returns:** Parsed analysis data

##### calculateStats()

```typescript
protected calculateStats(): Stats
```

Calculates statistics from the loaded issues.

**Returns:** Statistics object with issue counts and percentages

##### generateHtml()

```typescript
protected generateHtml(
  stats: Stats,
  issuesJsonl: string,
  codeJsonl: string,
  hasContext: boolean
): string
```

Generates the complete HTML document.

**Parameters:**
- `stats`: Calculated statistics
- `issuesJsonl`: Issues in JSONL format
- `codeJsonl`: Code context in JSONL format
- `hasContext`: Whether any issues have code context

**Returns:** Complete HTML document as string

## Types

### GeneratorOptions

Configuration options for the dashboard generator.

```typescript
interface GeneratorOptions {
  /** Path to input JSON file */
  input: string;
  
  /** Path to output HTML file (optional) */
  output?: string;
  
  /** Dashboard title (optional) */
  title?: string;
  
  /** Project name to display (optional) */
  projectName?: string;
  
  /** Custom configuration (optional) */
  config?: Partial<DashboardConfig>;
  
  /** Enable verbose logging (optional) */
  verbose?: boolean;
}
```

### DashboardConfig

Configuration for the virtual scrolling behavior.

```typescript
interface DashboardConfig {
  /** Height of each row in pixels (default: 50) */
  ROW_HEIGHT: number;
  
  /** Number of extra rows to render above/below viewport (default: 5) */
  VISIBLE_BUFFER: number;
  
  /** Debounce time for scroll events in milliseconds (default: 10) */
  SCROLL_DEBOUNCE: number;
  
  /** Debounce time for search input in milliseconds (default: 300) */
  SEARCH_DEBOUNCE: number;
  
  /** Number of issues to process at once (default: 50) */
  BATCH_SIZE: number;
}
```

### AnalysisData

Input data structure from cppcheck JSON output.

```typescript
interface AnalysisData {
  /** Array of all issues found */
  issues: Issue[];
  
  /** Optional timestamp of analysis */
  timestamp?: string;
  
  /** Optional metadata */
  metadata?: {
    tool?: string;
    version?: string;
    command?: string;
    [key: string]: any;
  };
}
```

### Issue

Represents a single issue found by cppcheck.

```typescript
interface Issue {
  /** Path to the file containing the issue */
  file?: string;
  
  /** Line number where the issue occurs */
  line?: string | number;
  
  /** Severity level of the issue */
  severity?: Severity | string;
  
  /** Description of the issue */
  message?: string;
  
  /** Unique identifier for the issue */
  id?: string;
  
  /** Optional code context showing the issue in its surrounding code */
  code_context?: CodeContext;
  
  /** Allow additional properties from cppcheck */
  [key: string]: any;
}
```

### CodeContext

Code context showing the issue with surrounding lines.

```typescript
interface CodeContext {
  /** Array of code lines around the issue */
  lines: CodeLine[];
}

interface CodeLine {
  /** Line number in the source file */
  number: number;
  
  /** Content of the line */
  content: string;
  
  /** Whether this is the line containing the issue */
  is_target?: boolean;
}
```

### Stats

Statistics calculated from the analysis.

```typescript
interface Stats {
  /** Total number of issues */
  total: number;
  
  /** Number of error-level issues */
  errors: number;
  
  /** Number of warning-level issues */
  warnings: number;
  
  /** Number of style issues */
  style: number;
  
  /** Number of performance issues */
  performance: number;
  
  /** Number of information issues */
  information: number;
  
  /** Percentage of errors */
  error_percent: number;
  
  /** Percentage of warnings */
  warning_percent: number;
  
  /** Percentage of style issues */
  style_percent: number;
  
  /** Percentage of performance issues */
  performance_percent: number;
}
```

### Severity

Severity levels for cppcheck issues.

```typescript
type Severity = 
  | 'error' 
  | 'warning' 
  | 'style' 
  | 'performance' 
  | 'information' 
  | 'portability' 
  | 'none';
```

## Functions

### generateStyles()

```typescript
function generateStyles(): string
```

Generates the complete CSS styles for the dashboard.

**Returns:** CSS string containing all dashboard styles

**Example:**
```typescript
const styles = generateStyles();
// Use in HTML: <style>${styles}</style>
```

### generateScripts()

```typescript
function generateScripts(config: DashboardConfig): string
```

Generates the JavaScript code for virtual scrolling and interactivity.

**Parameters:**
- `config`: Dashboard configuration

**Returns:** JavaScript code as string

**Example:**
```typescript
const scripts = generateScripts({
  ROW_HEIGHT: 50,
  VISIBLE_BUFFER: 5,
  SCROLL_DEBOUNCE: 10,
  SEARCH_DEBOUNCE: 300,
  BATCH_SIZE: 50
});
// Use in HTML: <script>${scripts}</script>
```

## Complete Example

```typescript
import { 
  StandaloneVirtualDashboardGenerator,
  type GeneratorOptions,
  type DashboardConfig,
  type AnalysisData
} from 'cppcheck-dashboard-generator';

async function generateDashboard() {
  // Custom configuration
  const config: Partial<DashboardConfig> = {
    ROW_HEIGHT: 60,
    VISIBLE_BUFFER: 10
  };

  // Generator options
  const options: GeneratorOptions = {
    input: 'cppcheck-results.json',
    output: 'analysis-dashboard.html',
    title: 'Code Quality Dashboard',
    projectName: 'My Project v2.0',
    config,
    verbose: true
  };

  // Create and run generator
  const generator = new StandaloneVirtualDashboardGenerator(options);
  
  try {
    await generator.generate();
    console.log('✅ Dashboard generated successfully');
  } catch (error) {
    console.error('❌ Generation failed:', error);
    process.exit(1);
  }
}

// Run the example
generateDashboard();
```

## Error Handling

The generator may throw errors in the following cases:

1. **File Not Found**: When the input file doesn't exist
2. **Invalid JSON**: When the input file contains invalid JSON
3. **Write Error**: When unable to write the output file
4. **Permission Error**: When lacking read/write permissions

Always wrap `generate()` calls in try-catch blocks:

```typescript
try {
  await generator.generate();
} catch (error) {
  if (error.message.includes('not found')) {
    console.error('Input file not found');
  } else if (error.message.includes('JSON')) {
    console.error('Invalid JSON format');
  } else {
    console.error('Unexpected error:', error);
  }
}
```