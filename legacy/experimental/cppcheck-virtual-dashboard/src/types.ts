export interface Issue {
  file?: string;
  line?: number;
  severity?: string;
  message?: string;
  id?: string;
  code_context?: CodeContext;
  [key: string]: any;
}

export interface CodeContext {
  lines?: CodeLine[];
  code?: string[];
  start_line?: number;
}

export interface CodeLine {
  number?: number;
  content?: string;
  is_target?: boolean;
}

export interface AnalysisData {
  issues: Issue[];
}

export interface Stats {
  total: number;
  errors: number;
  warnings: number;
  style: number;
  performance: number;
  information: number;
  error_percent: number;
  warning_percent: number;
  style_percent: number;
  performance_percent: number;
}

export interface GeneratorOptions {
  title?: string;
  projectName?: string;
}