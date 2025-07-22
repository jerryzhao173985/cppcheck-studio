import * as fs from 'fs';
import * as crypto from 'crypto';
import { Issue, AnalysisData, Stats, CodeContext, GeneratorOptions } from './types';
import { generateStyles } from './styles';
import { generateScripts } from './scripts';

export class StandaloneVirtualDashboardGenerator {
  private issues: Issue[] = [];
  private timestamp: string;

  constructor(private options: GeneratorOptions) {
    this.timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  }

  async generate(): Promise<void> {
    try {
      // Check if input file exists
      if (!fs.existsSync(this.options.input)) {
        throw new Error('Input file not found');
      }

      // Load and parse input JSON
      if (this.options.verbose) {
        console.log('Loading analysis data from:', this.options.input);
      }
      const data = await this.loadAnalysisData();
      this.issues = data.issues || [];

      // Generate unique IDs for each issue
      this.generateIssueIds();

      // Calculate statistics
      const stats = this.calculateStats();

      // Prepare data
      const { issuesWithoutContext, codeContextMap, withContext } = this.prepareData();

      // Generate JSONL strings
      const issuesJsonl = this.generateJsonl(issuesWithoutContext);
      const codeJsonl = this.generateCodeContextJsonl(codeContextMap);

      // Generate HTML
      const html = this.generateHtml(stats, issuesJsonl, codeJsonl, withContext);

      // Write output
      const outputFile = this.options.output || 'standalone-virtual-dashboard.html';
      await fs.promises.writeFile(outputFile, html, 'utf-8');

      // Print summary
      if (this.options.verbose) {
        console.log(`✅ Standalone virtual scroll dashboard generated: ${outputFile}`);
        console.log(`   Total issues: ${this.issues.length}`);
        console.log(`   Issues with code context: ${withContext}`);
        const fileSize = (await fs.promises.stat(outputFile)).size;
        console.log(`   File size: ${(fileSize / 1024 / 1024).toFixed(1)} MB`);
        console.log(`   No server required - works with file:// protocol`);
      }
    } catch (error) {
      console.error('Error generating dashboard:', error);
      throw error;
    }
  }

  private async loadAnalysisData(): Promise<AnalysisData> {
    const content = await fs.promises.readFile(this.options.input, 'utf-8');
    return JSON.parse(content);
  }

  private generateIssueIds(): void {
    this.issues.forEach(issue => {
      if (!issue.id) {
        const idStr = `${issue.file || ''}:${issue.line || ''}:${issue.message || ''}`;
        issue.id = crypto
          .createHash('md5')
          .update(idStr)
          .digest('hex')
          .substring(0, 8)
          .toUpperCase();
      }
    });
  }

  private calculateStats(): Stats {
    const total = this.issues.length;

    if (total === 0) {
      return {
        total: 0,
        errors: 0,
        warnings: 0,
        style: 0,
        performance: 0,
        information: 0,
        error_percent: 0,
        warning_percent: 0,
        style_percent: 0,
        performance_percent: 0,
      };
    }

    const stats: Stats = {
      total,
      errors: this.issues.filter(i => i.severity === 'error').length,
      warnings: this.issues.filter(i => i.severity === 'warning').length,
      style: this.issues.filter(i => i.severity === 'style').length,
      performance: this.issues.filter(i => i.severity === 'performance').length,
      information: this.issues.filter(i => i.severity === 'information').length,
      error_percent: 0,
      warning_percent: 0,
      style_percent: 0,
      performance_percent: 0,
    };

    // Calculate percentages
    stats.error_percent = (stats.errors / total) * 100;
    stats.warning_percent = (stats.warnings / total) * 100;
    stats.style_percent = (stats.style / total) * 100;
    stats.performance_percent = (stats.performance / total) * 100;

    return stats;
  }

  private prepareData(): {
    issuesWithoutContext: Issue[];
    codeContextMap: Map<string, CodeContext>;
    withContext: number;
  } {
    const issuesWithoutContext: Issue[] = [];
    const codeContextMap = new Map<string, CodeContext>();

    for (const issue of this.issues) {
      // Create issue without code context
      const issueCopy = { ...issue };
      delete issueCopy.code_context;
      issuesWithoutContext.push(issueCopy);

      // Store code context separately
      if (issue.code_context && issue.id) {
        codeContextMap.set(issue.id, issue.code_context);
      }
    }

    return {
      issuesWithoutContext,
      codeContextMap,
      withContext: codeContextMap.size,
    };
  }

  private generateJsonl(issues: Issue[]): string {
    // Join with a placeholder that won't break JavaScript parsing
    return issues.map(issue => JSON.stringify(issue)).join('__NEWLINE__');
  }

  private generateCodeContextJsonl(codeContextMap: Map<string, CodeContext>): string {
    const entries: string[] = [];
    for (const [id, context] of codeContextMap) {
      entries.push(JSON.stringify({ id, code_context: context }));
    }
    // Join with a placeholder that won't break JavaScript parsing
    return entries.join('__NEWLINE__');
  }

  private generateHtml(
    stats: Stats,
    issuesJsonl: string,
    codeJsonl: string,
    withContext: number
  ): string {
    const projectName = this.options.projectName || 'Project';
    const title = this.options.title || 'CPPCheck Studio - Virtual Scroll Dashboard';

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        ${generateStyles()}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <h1><i class="fas fa-code"></i> ${title}</h1>
                <div class="header-info">
                    <span><i class="fas fa-project-diagram"></i> ${projectName}</span>
                    <span><i class="fas fa-clock"></i> ${this.timestamp}</span>
                    <span><i class="fas fa-database"></i> ${this.issues.length} total issues</span>
                    <span><i class="fas fa-file-code"></i> ${withContext} with code context</span>
                </div>
            </div>
        </header>
        
        <!-- Statistics Cards -->
        <div class="stats-grid">
            <div class="stat-card error">
                <i class="fas fa-exclamation-circle"></i>
                <h3>Errors</h3>
                <div class="value">${stats.errors}</div>
                <div class="percent">${stats.error_percent.toFixed(1)}%</div>
            </div>
            
            <div class="stat-card warning">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Warnings</h3>
                <div class="value">${stats.warnings}</div>
                <div class="percent">${stats.warning_percent.toFixed(1)}%</div>
            </div>
            
            <div class="stat-card style">
                <i class="fas fa-palette"></i>
                <h3>Style</h3>
                <div class="value">${stats.style}</div>
                <div class="percent">${stats.style_percent.toFixed(1)}%</div>
            </div>
            
            <div class="stat-card performance">
                <i class="fas fa-tachometer-alt"></i>
                <h3>Performance</h3>
                <div class="value">${stats.performance}</div>
                <div class="percent">${stats.performance_percent.toFixed(1)}%</div>
            </div>
        </div>
        
        <!-- Filter Controls -->
        <div class="controls">
            <div class="search-container">
                <i class="fas fa-search"></i>
                <input type="text" id="searchInput" placeholder="Search by file, message, or ID..." onkeyup="debounce(filterData, 300)()">
            </div>
            
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="setSeverityFilter('all', this)">
                    <i class="fas fa-list"></i> All (${stats.total})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('error', this)">
                    <i class="fas fa-exclamation-circle"></i> Errors (${stats.errors})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('warning', this)">
                    <i class="fas fa-exclamation-triangle"></i> Warnings (${stats.warnings})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('style', this)">
                    <i class="fas fa-palette"></i> Style (${stats.style})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('performance', this)">
                    <i class="fas fa-tachometer-alt"></i> Performance (${stats.performance})
                </button>
                <button class="filter-btn" onclick="setSeverityFilter('information', this)">
                    <i class="fas fa-info-circle"></i> Info
                </button>
            </div>
        </div>
        
        <!-- Issues Count and Loading Status -->
        <div class="status-bar">
            <div class="issues-count">
                <span id="issuesCount">Loading...</span>
            </div>
            <div class="loading-status" id="loadingStatus" style="display: none;">
                <i class="fas fa-spinner fa-spin"></i> <span id="loadingText">Loading...</span>
            </div>
        </div>
        
        <!-- Virtual Scroll Container -->
        <div class="virtual-scroll-container" id="scrollContainer">
            <div class="issues-table-wrapper">
                <table class="issues-table">
                    <thead>
                        <tr>
                            <th class="col-indicator"></th>
                            <th class="col-file">FILE</th>
                            <th class="col-line">LINE</th>
                            <th class="col-severity">SEVERITY</th>
                            <th class="col-message">MESSAGE</th>
                            <th class="col-id">ID</th>
                            <th class="col-actions">ACTIONS</th>
                        </tr>
                    </thead>
                </table>
                <div class="virtual-scroll-viewport" id="viewport">
                    <div class="virtual-scroll-spacer" id="spacerTop"></div>
                    <table class="issues-table">
                        <tbody id="issuesBody">
                            <!-- Virtual rows will be rendered here -->
                        </tbody>
                    </table>
                    <div class="virtual-scroll-spacer" id="spacerBottom"></div>
                </div>
            </div>
        </div>
        
        <!-- Code Preview Modal -->
        <div id="codeModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 id="modalTitle">Issue Details</h3>
                    <button onclick="closeModal()" class="close-btn">&times;</button>
                </div>
                <div class="modal-body" id="modalBody">
                    <!-- Content will be inserted here -->
                </div>
            </div>
        </div>
    </div>
    
    <!-- Embedded JSONL Data -->
    <script id="issuesData" type="application/x-ndjson">
${issuesJsonl}
    </script>
    
    <script id="codeContextData" type="application/x-ndjson">
${codeJsonl}
    </script>
    
    <script>
        ${generateScripts()}
    </script>
</body>
</html>`;
  }
}
