import chalk from 'chalk'
import { CppcheckAnalyzer } from '@cppcheck-studio/core'
import path from 'path'

export async function checkCommand(projectPath: string = '.', options: any) {
  try {
    const analyzer = new CppcheckAnalyzer({
      projectPath: path.resolve(projectPath),
      profile: 'full'
    })

    const results = await analyzer.analyze()
    
    // Count issues by severity
    const severityCounts = results.summary.bySeverity
    const errorCount = severityCounts.error || 0
    const warningCount = severityCounts.warning || 0
    
    // Format output based on CI system
    if (options.format === 'github') {
      formatGitHubOutput(results.issues)
    } else if (options.format === 'junit') {
      console.log(formatJUnitOutput(results))
    } else {
      // Default text output
      console.log(`CPPCheck found ${results.issues.length} issues:`)
      console.log(`  Errors: ${errorCount}`)
      console.log(`  Warnings: ${warningCount}`)
      console.log(`  Style: ${severityCounts.style || 0}`)
      console.log(`  Performance: ${severityCounts.performance || 0}`)
    }
    
    // Determine exit code based on threshold
    let shouldFail = false
    switch (options.threshold) {
      case 'error':
        shouldFail = errorCount > 0
        break
      case 'warning':
        shouldFail = errorCount > 0 || warningCount > 0
        break
      case 'any':
        shouldFail = results.issues.length > 0
        break
    }
    
    if (shouldFail) {
      console.error(chalk.red(`\n✗ Code quality check failed`))
      process.exit(1)
    } else {
      console.log(chalk.green(`\n✓ Code quality check passed`))
    }
    
  } catch (error: any) {
    console.error(chalk.red(`Check failed: ${error.message}`))
    process.exit(1)
  }
}

function formatGitHubOutput(issues: any[]) {
  // GitHub Actions annotation format
  for (const issue of issues) {
    const level = issue.severity === 'error' ? 'error' : 
                 issue.severity === 'warning' ? 'warning' : 'notice'
    
    console.log(
      `::{level} file={file},line={line},col={col}::{message}`
        .replace('{level}', level)
        .replace('{file}', issue.file)
        .replace('{line}', issue.line.toString())
        .replace('{col}', (issue.column || 0).toString())
        .replace('{message}', `[${issue.id}] ${issue.message}`)
    )
  }
}

function formatJUnitOutput(results: any): string {
  const testsuites = {
    name: 'CPPCheck Analysis',
    tests: results.issues.length,
    failures: results.summary.bySeverity.error || 0,
    errors: 0,
    time: 0
  }
  
  const testcases = results.issues.map((issue: any) => {
    const failure = issue.severity === 'error' ? {
      message: issue.message,
      type: issue.id,
      text: `${issue.file}:${issue.line}:${issue.column || 0}`
    } : null
    
    return {
      name: `${issue.file}:${issue.line}`,
      classname: issue.id,
      time: 0,
      failure
    }
  })
  
  // Simple XML generation
  return `<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="${testsuites.name}" tests="${testsuites.tests}" failures="${testsuites.failures}" errors="${testsuites.errors}" time="${testsuites.time}">
  <testsuite name="CPPCheck" tests="${testsuites.tests}" failures="${testsuites.failures}" errors="${testsuites.errors}" time="${testsuites.time}">
    ${testcases.map((tc: any) => `
    <testcase name="${tc.name}" classname="${tc.classname}" time="${tc.time}">
      ${tc.failure ? `<failure message="${tc.failure.message}" type="${tc.failure.type}">${tc.failure.text}</failure>` : ''}
    </testcase>`).join('')}
  </testsuite>
</testsuites>`
}