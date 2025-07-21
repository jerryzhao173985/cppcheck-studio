import chalk from 'chalk'
import inquirer from 'inquirer'
import { promises as fs } from 'fs'
import path from 'path'

const defaultConfig = {
  profile: 'cpp17',
  paths: ['src', 'include'],
  exclude: ['build/**', 'third_party/**', 'vendor/**'],
  incremental: true,
  autoFix: {
    enabled: true,
    confidence: 85,
    types: ['nullptr', 'override', 'explicit', 'auto']
  },
  customRules: [],
  suppressions: [
    'missingInclude:*/external/*',
    'unmatchedSuppression'
  ]
}

export async function initCommand() {
  console.log(chalk.bold('🚀 Welcome to CPPCheck Studio!\n'))
  console.log('This utility will help you create a configuration file.\n')

  try {
    // Check if config already exists
    const configPath = path.join(process.cwd(), '.cppcheckstudio.json')
    let existingConfig = null
    
    try {
      const existing = await fs.readFile(configPath, 'utf8')
      existingConfig = JSON.parse(existing)
      
      const { overwrite } = await inquirer.prompt([{
        type: 'confirm',
        name: 'overwrite',
        message: 'Configuration file already exists. Overwrite?',
        default: false
      }])
      
      if (!overwrite) {
        console.log(chalk.yellow('Configuration unchanged.'))
        return
      }
    } catch {
      // No existing config
    }

    // Ask configuration questions
    const answers = await inquirer.prompt([
      {
        type: 'list',
        name: 'profile',
        message: 'Select analysis profile:',
        choices: [
          { name: 'Quick (development)', value: 'quick' },
          { name: 'Full (comprehensive)', value: 'full' },
          { name: 'C++17 modernization', value: 'cpp17' },
          { name: 'C++20 features', value: 'cpp20' },
          { name: 'Memory safety', value: 'memory' },
          { name: 'Performance', value: 'performance' }
        ],
        default: existingConfig?.profile || 'cpp17'
      },
      {
        type: 'input',
        name: 'paths',
        message: 'Source directories (comma-separated):',
        default: (existingConfig?.paths || defaultConfig.paths).join(', '),
        filter: (input: string) => input.split(',').map(p => p.trim()).filter(Boolean)
      },
      {
        type: 'input',
        name: 'exclude',
        message: 'Exclude patterns (comma-separated):',
        default: (existingConfig?.exclude || defaultConfig.exclude).join(', '),
        filter: (input: string) => input.split(',').map(p => p.trim()).filter(Boolean)
      },
      {
        type: 'confirm',
        name: 'incremental',
        message: 'Enable incremental analysis?',
        default: existingConfig?.incremental ?? defaultConfig.incremental
      },
      {
        type: 'confirm',
        name: 'autoFixEnabled',
        message: 'Enable automatic fixes?',
        default: existingConfig?.autoFix?.enabled ?? defaultConfig.autoFix.enabled
      }
    ])

    // Additional questions for auto-fix
    let autoFixConfig = defaultConfig.autoFix
    if (answers.autoFixEnabled) {
      const fixAnswers = await inquirer.prompt([
        {
          type: 'number',
          name: 'confidence',
          message: 'Minimum confidence for auto-fixes (0-100):',
          default: existingConfig?.autoFix?.confidence ?? defaultConfig.autoFix.confidence,
          validate: (input: number) => input >= 0 && input <= 100
        },
        {
          type: 'checkbox',
          name: 'types',
          message: 'Select fix types to enable:',
          choices: [
            { name: 'nullptr (NULL → nullptr)', value: 'nullptr', checked: true },
            { name: 'override (add override specifier)', value: 'override', checked: true },
            { name: 'explicit (add explicit to constructors)', value: 'explicit', checked: true },
            { name: 'auto (use auto for obvious types)', value: 'auto', checked: true },
            { name: 'range-for (modernize loops)', value: 'range-for', checked: false },
            { name: 'using (typedef → using)', value: 'using', checked: false }
          ]
        }
      ])
      
      autoFixConfig = {
        enabled: true,
        confidence: fixAnswers.confidence,
        types: fixAnswers.types
      }
    }

    // Create configuration
    const config = {
      profile: answers.profile,
      paths: answers.paths,
      exclude: answers.exclude,
      incremental: answers.incremental,
      autoFix: autoFixConfig,
      customRules: existingConfig?.customRules || [],
      suppressions: existingConfig?.suppressions || defaultConfig.suppressions
    }

    // Write configuration file
    await fs.writeFile(configPath, JSON.stringify(config, null, 2))
    
    console.log(chalk.green('\n✓ Configuration saved to .cppcheckstudio.json'))
    
    // Show next steps
    console.log('\n' + chalk.bold('Next steps:'))
    console.log('  1. Run ' + chalk.cyan('cppcheck-studio analyze') + ' to analyze your project')
    console.log('  2. Run ' + chalk.cyan('cppcheck-studio start') + ' to open the web interface')
    console.log('  3. Run ' + chalk.cyan('cppcheck-studio fix --dry-run') + ' to preview fixes')
    
    // Offer to create pre-commit hook
    const { createHook } = await inquirer.prompt([{
      type: 'confirm',
      name: 'createHook',
      message: 'Create a pre-commit hook?',
      default: true
    }])
    
    if (createHook) {
      await createPreCommitHook()
    }
    
  } catch (error: any) {
    console.error(chalk.red(`Initialization failed: ${error.message}`))
    process.exit(1)
  }
}

async function createPreCommitHook() {
  const hookPath = path.join(process.cwd(), '.git', 'hooks', 'pre-commit')
  const hookContent = `#!/bin/sh
# CPPCheck Studio pre-commit hook

# Run quick analysis on staged files
files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\\.(cpp|hpp|cc|h|cxx|hxx)$')

if [ -n "$files" ]; then
  echo "Running CPPCheck Studio analysis..."
  npx cppcheck-studio check --threshold error --format text
  
  if [ $? -ne 0 ]; then
    echo "❌ Fix C++ issues before committing"
    echo "Run 'cppcheck-studio fix' to apply automatic fixes"
    exit 1
  fi
fi
`

  try {
    await fs.mkdir(path.dirname(hookPath), { recursive: true })
    await fs.writeFile(hookPath, hookContent)
    await fs.chmod(hookPath, '755')
    console.log(chalk.green('✓ Pre-commit hook created'))
  } catch (error) {
    console.log(chalk.yellow('Could not create pre-commit hook (not a git repository?)'))
  }
}