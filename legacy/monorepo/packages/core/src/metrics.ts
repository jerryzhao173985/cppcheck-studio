import { CppcheckIssue } from './types'
import path from 'path'
import { promises as fs } from 'fs'

export interface MetricsSummary {
  totalIssues: number
  bySeverity: Record<string, number>
  byCategory: Record<string, number>
  byFile: Record<string, number>
  fixApplied: number
  fixAvailable: number
}

export interface MetricsTrend {
  date: string
  issues: number
  fixed: number
  new: number
}

export interface MetricsOptions {
  projectId?: string
  startDate?: Date
  endDate?: Date
  groupBy?: 'day' | 'week' | 'month'
}

export class MetricsCollector {
  private metricsPath: string

  constructor(basePath?: string) {
    this.metricsPath = path.join(basePath || process.cwd(), 'data', 'metrics')
  }

  async collectFromIssues(issues: CppcheckIssue[], projectId?: string): Promise<MetricsSummary> {
    const summary: MetricsSummary = {
      totalIssues: issues.length,
      bySeverity: {},
      byCategory: {},
      byFile: {},
      fixApplied: 0,
      fixAvailable: 0
    }

    // Count by severity
    for (const issue of issues) {
      summary.bySeverity[issue.severity] = (summary.bySeverity[issue.severity] || 0) + 1
      
      // Extract category from ID (e.g., "nullPointer" -> "safety")
      const category = this.getCategory(issue.id)
      summary.byCategory[category] = (summary.byCategory[category] || 0) + 1
      
      // Count by file
      const fileName = path.basename(issue.file)
      summary.byFile[fileName] = (summary.byFile[fileName] || 0) + 1
      
      // Check if fix is available
      if (this.hasAvailableFix(issue.id)) {
        summary.fixAvailable++
      }
    }

    // Save metrics
    await this.saveMetrics(summary, projectId)

    return summary
  }

  async getMetrics(options: MetricsOptions = {}): Promise<any> {
    const metricsFile = path.join(this.metricsPath, 'history.json')
    
    try {
      await fs.mkdir(this.metricsPath, { recursive: true })
      const data = await fs.readFile(metricsFile, 'utf8')
      const history = JSON.parse(data)
      
      // Filter by options
      let filtered = history
      
      if (options.projectId) {
        filtered = filtered.filter((m: any) => m.projectId === options.projectId)
      }
      
      if (options.startDate) {
        filtered = filtered.filter((m: any) => new Date(m.date) >= options.startDate!)
      }
      
      if (options.endDate) {
        filtered = filtered.filter((m: any) => new Date(m.date) <= options.endDate!)
      }
      
      // Group by period
      if (options.groupBy) {
        return this.groupByPeriod(filtered, options.groupBy)
      }
      
      return filtered
    } catch (error) {
      return []
    }
  }

  async getSummary(options: { projectId?: string } = {}): Promise<any> {
    const metrics = await this.getMetrics(options)
    
    if (metrics.length === 0) {
      return {
        totalIssues: 0,
        totalFixed: 0,
        averageIssuesPerFile: 0,
        mostCommonSeverity: 'none',
        mostCommonCategory: 'none'
      }
    }
    
    const latest = metrics[metrics.length - 1]
    const totalFixed = metrics.reduce((sum: number, m: any) => sum + (m.fixApplied || 0), 0)
    
    return {
      totalIssues: latest.totalIssues,
      totalFixed,
      averageIssuesPerFile: this.calculateAveragePerFile(latest),
      mostCommonSeverity: this.getMostCommon(latest.bySeverity),
      mostCommonCategory: this.getMostCommon(latest.byCategory),
      trend: this.calculateTrend(metrics)
    }
  }

  async getTrends(options: { projectId?: string; days?: number } = {}): Promise<MetricsTrend[]> {
    const endDate = new Date()
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - (options.days || 30))
    
    const metrics = await this.getMetrics({
      projectId: options.projectId,
      startDate,
      endDate
    })
    
    const trends: MetricsTrend[] = []
    
    for (let i = 0; i < metrics.length; i++) {
      const current = metrics[i]
      const previous = i > 0 ? metrics[i - 1] : null
      
      trends.push({
        date: current.date,
        issues: current.totalIssues,
        fixed: current.fixApplied || 0,
        new: previous ? Math.max(0, current.totalIssues - previous.totalIssues + current.fixApplied) : current.totalIssues
      })
    }
    
    return trends
  }

  async export(options: { format: 'csv' | 'json'; projectId?: string }): Promise<string> {
    const metrics = await this.getMetrics({ projectId: options.projectId })
    
    if (options.format === 'json') {
      return JSON.stringify(metrics, null, 2)
    }
    
    // CSV export
    const headers = ['Date', 'Total Issues', 'Errors', 'Warnings', 'Style', 'Performance', 'Fixed']
    const rows = metrics.map((m: any) => [
      m.date,
      m.totalIssues,
      m.bySeverity.error || 0,
      m.bySeverity.warning || 0,
      m.bySeverity.style || 0,
      m.bySeverity.performance || 0,
      m.fixApplied || 0
    ])
    
    const csv = [headers, ...rows].map(row => row.join(',')).join('\n')
    return csv
  }

  private async saveMetrics(summary: MetricsSummary, projectId?: string): Promise<void> {
    const metricsFile = path.join(this.metricsPath, 'history.json')
    
    try {
      await fs.mkdir(this.metricsPath, { recursive: true })
      
      let history = []
      try {
        const data = await fs.readFile(metricsFile, 'utf8')
        history = JSON.parse(data)
      } catch (error) {
        // File doesn't exist yet
      }
      
      const entry = {
        ...summary,
        date: new Date().toISOString(),
        projectId
      }
      
      history.push(entry)
      
      // Keep only last 365 days
      const cutoffDate = new Date()
      cutoffDate.setDate(cutoffDate.getDate() - 365)
      history = history.filter((h: any) => new Date(h.date) > cutoffDate)
      
      await fs.writeFile(metricsFile, JSON.stringify(history, null, 2))
    } catch (error) {
      console.error('Failed to save metrics:', error)
    }
  }

  private getCategory(issueId: string): string {
    const categoryMap: Record<string, string> = {
      // Safety
      nullPointer: 'safety',
      uninitvar: 'safety',
      memleak: 'safety',
      resourceLeak: 'safety',
      useInitializedVariable: 'safety',
      
      // Modernization
      useStlAlgorithm: 'modernization',
      modernizeUseNullptr: 'modernization',
      modernizeUseOverride: 'modernization',
      modernizeUseAuto: 'modernization',
      passedByValue: 'modernization',
      
      // Performance
      stlSize: 'performance',
      redundantAssignment: 'performance',
      redundantCondition: 'performance',
      
      // Style
      variableScope: 'style',
      unreadVariable: 'style',
      unusedFunction: 'style',
      redundantIfRemove: 'style'
    }
    
    for (const [pattern, category] of Object.entries(categoryMap)) {
      if (issueId.toLowerCase().includes(pattern.toLowerCase())) {
        return category
      }
    }
    
    return 'other'
  }

  private hasAvailableFix(issueId: string): boolean {
    const fixableIssues = [
      'modernizeUseNullptr',
      'modernizeUseOverride',
      'modernizeUseAuto',
      'passedByValue',
      'useStlAlgorithm',
      'redundantIfRemove',
      'variableScope'
    ]
    
    return fixableIssues.some(fixable => 
      issueId.toLowerCase().includes(fixable.toLowerCase())
    )
  }

  private groupByPeriod(metrics: any[], period: 'day' | 'week' | 'month'): any[] {
    const grouped: Record<string, any> = {}
    
    for (const metric of metrics) {
      const date = new Date(metric.date)
      let key: string
      
      switch (period) {
        case 'day':
          key = date.toISOString().split('T')[0]
          break
        case 'week':
          const weekStart = new Date(date)
          weekStart.setDate(date.getDate() - date.getDay())
          key = weekStart.toISOString().split('T')[0]
          break
        case 'month':
          key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
          break
      }
      
      if (!grouped[key]) {
        grouped[key] = {
          date: key,
          totalIssues: 0,
          fixApplied: 0,
          count: 0
        }
      }
      
      grouped[key].totalIssues += metric.totalIssues
      grouped[key].fixApplied += metric.fixApplied || 0
      grouped[key].count++
    }
    
    // Average the values
    return Object.values(grouped).map(g => ({
      date: g.date,
      totalIssues: Math.round(g.totalIssues / g.count),
      fixApplied: g.fixApplied
    }))
  }

  private calculateAveragePerFile(metrics: any): number {
    const fileCount = Object.keys(metrics.byFile || {}).length
    return fileCount > 0 ? Math.round(metrics.totalIssues / fileCount) : 0
  }

  private getMostCommon(counts: Record<string, number>): string {
    if (!counts || Object.keys(counts).length === 0) {
      return 'none'
    }
    
    return Object.entries(counts)
      .sort(([, a], [, b]) => b - a)[0][0]
  }

  private calculateTrend(metrics: any[]): 'improving' | 'worsening' | 'stable' {
    if (metrics.length < 2) {
      return 'stable'
    }
    
    const recent = metrics.slice(-7)
    const older = metrics.slice(-14, -7)
    
    const recentAvg = recent.reduce((sum, m) => sum + m.totalIssues, 0) / recent.length
    const olderAvg = older.reduce((sum, m) => sum + m.totalIssues, 0) / Math.max(older.length, 1)
    
    const change = ((recentAvg - olderAvg) / olderAvg) * 100
    
    if (change < -5) return 'improving'
    if (change > 5) return 'worsening'
    return 'stable'
  }
}