import chalk from 'chalk'
import ora from 'ora'
import inquirer from 'inquirer'
import { CppcheckAnalyzer, FixGenerator } from '@cppcheck-studio/core'
import path from 'path'

export async function fixCommand(projectPath: string = '.', options: any) {
  const spinner = ora('Analyzing project for fixes...').start()

  try {
    // Run analysis first
    const analyzer = new CppcheckAnalyzer({
      projectPath: path.resolve(projectPath),
      profile: 'cpp17'
    })

    const results = await analyzer.analyze()
    spinner.stop()

    // Filter fixable issues
    const fixGenerator = new FixGenerator()
    const fixableIssues = results.issues.filter(issue => 
      fixGenerator.canFix(issue.id)
    )

    if (fixableIssues.length === 0) {
      console.log(chalk.yellow('No automatically fixable issues found.'))
      return
    }

    console.log(chalk.blue(`Found ${fixableIssues.length} fixable issues`))

    // Filter by confidence if specified
    const confidenceThreshold = parseInt(options.confidence)
    let issuesToFix = fixableIssues

    if (options.types && options.types.length > 0) {
      issuesToFix = issuesToFix.filter(issue =>
        options.types.some((type: string) => issue.id.includes(type))
      )
    }

    // Interactive mode
    if (options.interactive) {
      issuesToFix = await selectIssuesInteractively(issuesToFix)
    }

    if (issuesToFix.length === 0) {
      console.log(chalk.yellow('No issues selected for fixing.'))
      return
    }

    // Generate fixes
    const fixes = []
    for (const issue of issuesToFix) {
      const fix = await fixGenerator.generateFix(issue)
      if (fix && fix.confidence >= confidenceThreshold) {
        fixes.push(fix)
      }
    }

    console.log(chalk.blue(`Generated ${fixes.length} fixes`))

    // Show preview if dry-run
    if (options.dryRun) {
      console.log('\n' + chalk.bold('Preview of changes:'))
      for (const fix of fixes) {
        console.log(`\n${chalk.cyan(fix.file)}:`)
        console.log(fix.diff)
      }
      
      if (!options.interactive) {
        return
      }

      const { proceed } = await inquirer.prompt([{
        type: 'confirm',
        name: 'proceed',
        message: 'Apply these fixes?',
        default: false
      }])

      if (!proceed) {
        console.log(chalk.yellow('Fixes not applied.'))
        return
      }
    }

    // Apply fixes
    const applySpinner = ora('Applying fixes...').start()
    const result = await fixGenerator.applyFixes(fixes, { dryRun: false })
    applySpinner.succeed(chalk.green(`Applied ${result.applied.length} fixes`))

    if (result.failed.length > 0) {
      console.log(chalk.red(`Failed to apply ${result.failed.length} fixes`))
    }

    console.log(chalk.gray(`Backup saved to: ${result.backupPath}`))

  } catch (error: any) {
    spinner.fail(chalk.red(`Fix command failed: ${error.message}`))
    process.exit(1)
  }
}

async function selectIssuesInteractively(issues: any[]): Promise<any[]> {
  const choices = issues.map((issue, index) => ({
    name: `${issue.severity.toUpperCase()} - ${issue.file}:${issue.line} - ${issue.message}`,
    value: index,
    checked: true
  }))

  const { selected } = await inquirer.prompt([{
    type: 'checkbox',
    name: 'selected',
    message: 'Select issues to fix:',
    choices,
    pageSize: 10
  }])

  return selected.map((index: number) => issues[index])
}