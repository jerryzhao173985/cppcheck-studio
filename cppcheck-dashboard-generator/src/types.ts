/**
 * Type definitions for CPPCheck Dashboard Generator
 */

/**
 * Severity levels for CPPCheck issues
 */
export type Severity =
  | 'error'
  | 'warning'
  | 'style'
  | 'performance'
  | 'information'
  | 'portability'
  | 'none';

/**
 * Represents a single issue found by CPPCheck
 */
export interface Issue {
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
  /** Allow additional properties from CPPCheck */
  [key: string]: any;
}

/**
 * Code context showing the issue with surrounding lines
 */
export interface CodeContext {
  /** Array of code lines around the issue */
  lines: CodeLine[];
}

/**
 * Represents a single line of code in the context
 */
export interface CodeLine {
  /** Line number in the source file */
  number: number;
  /** Content of the line */
  content: string;
  /** Whether this is the line containing the issue */
  is_target?: boolean;
}

/**
 * Input data structure from CPPCheck JSON output
 */
export interface AnalysisData {
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

/**
 * Statistics calculated from the analysis
 */
export interface Stats {
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

/**
 * Configuration for the virtual scrolling dashboard
 */
export interface DashboardConfig {
  /** Height of each row in pixels */
  ROW_HEIGHT: number;
  /** Number of extra rows to render above/below viewport */
  VISIBLE_BUFFER: number;
  /** Debounce time for scroll events in milliseconds */
  SCROLL_DEBOUNCE: number;
  /** Debounce time for search input in milliseconds */
  SEARCH_DEBOUNCE: number;
  /** Number of issues to process at once */
  BATCH_SIZE: number;
}

/**
 * Options for the dashboard generator
 */
export interface GeneratorOptions {
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

/**
 * Result of dashboard generation
 */
export interface GeneratorResult {
  /** Path to generated file */
  outputPath: string;
  /** Statistics about the generation */
  stats: {
    issueCount: number;
    issuesWithContext: number;
    fileSize: number;
    generationTime: number;
  };
}

/**
 * Options for programmatic API usage
 */
export interface APIOptions extends Omit<GeneratorOptions, 'input'> {
  /** Analysis data object (alternative to file input) */
  data?: AnalysisData;
  /** Input file path (alternative to data object) */
  inputFile?: string;
}

/**
 * Filter state for the dashboard
 */
export interface FilterState {
  /** Current severity filter */
  severity: Severity | 'all';
  /** Current search term */
  searchTerm: string;
  /** Whether to show only issues with code context */
  onlyWithContext?: boolean;
}

/**
 * Virtual scroll state
 */
export interface ScrollState {
  /** All issues */
  allIssues: Issue[];
  /** Filtered issues based on current filters */
  filteredIssues: Issue[];
  /** Map of issue ID to code context */
  codeContextMap: Map<string, CodeContext>;
  /** Current filter state */
  currentFilter: string;
  /** Current search term */
  currentSearch: string;
  /** Index of first visible row */
  visibleStart: number;
  /** Index of last visible row */
  visibleEnd: number;
  /** Whether data is loading */
  isLoading: boolean;
  /** Current scroll position */
  scrollTop: number;
  /** Height of the container */
  containerHeight: number;
}
