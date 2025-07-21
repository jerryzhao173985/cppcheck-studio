import chalk from 'chalk'
import ora from 'ora'
import { CppcheckAnalyzer } from '@cppcheck-studio/core'
import { promises as fs } from 'fs'
import path from 'path'

export async function analyzeCommand(projectPath: string = '.', options: any) {
  const spinner = ora('Analyzing project...').start()

  try {
    const analyzer = new CppcheckAnalyzer({
      projectPath: path.resolve(projectPath),
      profile: options.profile,
      incremental: options.incremental,
      exclude: options.exclude
    })

    // Run analysis
    const results = await analyzer.analyze()
    spinner.succeed(`Analysis complete: ${results.issues.length} issues found`)

    // Format output
    let output: string
    switch (options.format) {
      case 'json':
        output = JSON.stringify(results, null, 2)
        break
      case 'html':
        output = await generateHtmlReport(results)
        break
      default:
        output = formatTextOutput(results)
    }

    // Save or print output
    if (options.output) {
      await fs.writeFile(options.output, output)
      console.log(chalk.green(`Report saved to ${options.output}`))
    } else {
      console.log(output)
    }

    // Show summary
    if (options.format === 'text') {
      console.log('\n' + chalk.bold('Summary:'))
      console.log(`  Errors: ${chalk.red(results.summary.bySeverity.error || 0)}`)
      console.log(`  Warnings: ${chalk.yellow(results.summary.bySeverity.warning || 0)}`)
      console.log(`  Style: ${chalk.blue(results.summary.bySeverity.style || 0)}`)
      console.log(`  Performance: ${chalk.magenta(results.summary.bySeverity.performance || 0)}`)
    }

  } catch (error: any) {
    spinner.fail(chalk.red(`Analysis failed: ${error.message}`))
    process.exit(1)
  }
}

function formatTextOutput(results: any): string {
  const lines: string[] = []
  
  for (const issue of results.issues) {
    const severity = issue.severity.toUpperCase()
    const color = getSeverityColor(issue.severity)
    
    lines.push(
      `${color(`[${severity}]`)} ${issue.file}:${issue.line}:${issue.column || 0} - ${issue.message} (${issue.id})`
    )
  }
  
  return lines.join('\n')
}

function getSeverityColor(severity: string): typeof chalk {
  switch (severity) {
    case 'error':
      return chalk.red
    case 'warning':
      return chalk.yellow
    case 'style':
      return chalk.blue
    case 'performance':
      return chalk.magenta
    default:
      return chalk.gray
  }
}

async function generateHtmlReport(results: any): Promise<string> {
  // Simple HTML report template
  return `
<!DOCTYPE html>
<html>
<head>
  <title>CPPCheck Studio Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .issue { margin: 10px 0; padding: 10px; border-left: 3px solid; }
    .error { border-color: #f44336; background: #ffebee; }
    .warning { border-color: #ff9800; background: #fff3e0; }
    .style { border-color: #2196f3; background: #e3f2fd; }
    .performance { border-color: #9c27b0; background: #f3e5f5; }
  </style>
</head>
<body>
  <h1>CPPCheck Studio Analysis Report</h1>
  <p>Total issues: ${results.issues.length}</p>
  ${results.issues.map((issue: any) => `
    <div class="issue ${issue.severity}">
      <strong>[${issue.severity.toUpperCase()}]</strong> 
      ${issue.file}:${issue.line}:${issue.column || 0}<br>
      ${issue.message} (${issue.id})
    </div>
  `).join('')}
</body>
</html>
  `
}