export interface CppcheckIssue {
  id: string
  file: string
  line: number
  column?: number
  severity: 'error' | 'warning' | 'style' | 'performance' | 'portability' | 'information'
  message: string
  verbose?: string
  cwe?: number
  hash?: string
}

export interface CodeContext {
  file: string
  targetLine: number
  lines: CodeLine[]
  function?: string
  class?: {
    name: string
    type: 'class' | 'struct'
  }
  language: string
}

export interface CodeLine {
  number: number
  content: string
  isTarget: boolean
  indent: number
}

export interface FixSuggestion {
  id: string
  issueId: string
  description: string
  confidence: number
  diff: string
  fixedLines?: CodeLine[]
  explanation: string
  manualReview?: boolean
}

export interface AnalysisConfig {
  projectPath?: string
  profile: 'quick' | 'full' | 'cpp17' | 'cpp20' | 'memory' | 'performance'
  paths?: string[]
  exclude?: string[]
  incremental?: boolean
  threads?: number
  suppressions?: string[]
  customRules?: string[]
  cppcheckBinary?: string
}

// Alias for compatibility
export type AnalysisOptions = AnalysisConfig

export interface AnalysisResult {
  id?: string
  issues: CppcheckIssue[]
  summary?: MetricsSummary
  stats?: {
    filesAnalyzed: number
    timeElapsed: number
    errors: number
    warnings: number
    style: number
    performance: number
    portability: number
    information: number
  }
  profile?: string
  timestamp?: string
  duration?: number
  filesAnalyzed?: number
}

export interface Project {
  id: string
  name: string
  path: string
  gitUrl?: string
  branch?: string
  lastAnalysis?: Date
  settings: ProjectSettings
}

export interface ProjectSettings {
  analysisProfile: AnalysisConfig['profile']
  autoFix: boolean
  includePatterns: string[]
  excludePatterns: string[]
  customRules: string[]
}