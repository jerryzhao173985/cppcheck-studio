import { CppcheckIssue } from './types'

export class CppcheckParser {
  parse(output: string): CppcheckIssue[] {
    const issues: CppcheckIssue[] = []
    const lines = output.split('\n').filter(line => line.trim())

    for (const line of lines) {
      // Skip non-issue lines
      if (line.includes('Checking') || line.includes('files checked') || !line.includes(':')) {
        continue
      }

      const issue = this.parseLine(line)
      if (issue) {
        issues.push(issue)
      }
    }

    return issues
  }

  private parseLine(line: string): CppcheckIssue | null {
    // Format: {file}:{line}:{column}: [{severity}:{id}] {message}
    const match = line.match(/^(.+?):(\d+):(\d+)?: \[(\w+):?([^\]]*)\] (.+)$/)
    
    if (!match) {
      // Try alternative format without column
      const altMatch = line.match(/^(.+?):(\d+): \[(\w+):?([^\]]*)\] (.+)$/)
      if (!altMatch) {
        return null
      }

      return {
        id: altMatch[4] || 'unknown',
        file: altMatch[1],
        line: parseInt(altMatch[2], 10),
        severity: this.normalizeSeverity(altMatch[3]),
        message: altMatch[5],
      }
    }

    return {
      id: match[5] || 'unknown',
      file: match[1],
      line: parseInt(match[2], 10),
      column: match[3] ? parseInt(match[3], 10) : undefined,
      severity: this.normalizeSeverity(match[4]),
      message: match[6],
    }
  }

  private normalizeSeverity(severity: string): CppcheckIssue['severity'] {
    const normalizedSeverity = severity.toLowerCase()
    const validSeverities: CppcheckIssue['severity'][] = [
      'error',
      'warning',
      'style',
      'performance',
      'portability',
      'information'
    ]

    if (validSeverities.includes(normalizedSeverity as CppcheckIssue['severity'])) {
      return normalizedSeverity as CppcheckIssue['severity']
    }

    // Map common alternatives
    if (normalizedSeverity === 'info') return 'information'
    if (normalizedSeverity === 'perf') return 'performance'
    
    return 'information'
  }

  parseXml(xmlContent: string): CppcheckIssue[] {
    // XML parsing for future enhancement
    // This would parse cppcheck's XML output format
    throw new Error('XML parsing not yet implemented')
  }
}