#!/usr/bin/env node

import { Command } from 'commander'
import chalk from 'chalk'
import ora from 'ora'
import inquirer from 'inquirer'
import { CppcheckAnalyzer } from '@cppcheck-studio/core'
import updateNotifier from 'update-notifier'
import { promises as fs } from 'fs'
import path from 'path'
import { startCommand } from './commands/start'
import { analyzeCommand } from './commands/analyze'
import { fixCommand } from './commands/fix'
import { checkCommand } from './commands/check'
import { initCommand } from './commands/init'

// Check for updates
const pkg = JSON.parse(
  await fs.readFile(new URL('../package.json', import.meta.url), 'utf8')
)
updateNotifier({ pkg }).notify()

const program = new Command()

program
  .name('cppcheck-studio')
  .description('Professional C++ Static Analysis Studio')
  .version(pkg.version)

// Start web interface
program
  .command('start')
  .description('Start the CPPCheck Studio web interface')
  .option('-p, --port <port>', 'Port to run on', '3000')
  .option('-o, --open', 'Open browser automatically', true)
  .option('--project <path>', 'Project path to analyze')
  .action(startCommand)

// Analyze command
program
  .command('analyze [path]')
  .description('Analyze a C++ project')
  .option('-p, --profile <profile>', 'Analysis profile', 'quick')
  .option('-f, --format <format>', 'Output format (json, html, text)', 'text')
  .option('-o, --output <file>', 'Output file')
  .option('--incremental', 'Use incremental analysis', true)
  .option('--exclude <patterns...>', 'Exclude patterns')
  .action(analyzeCommand)

// Fix command
program
  .command('fix [path]')
  .description('Apply fixes to C++ code issues')
  .option('--dry-run', 'Preview fixes without applying', true)
  .option('--confidence <threshold>', 'Minimum confidence threshold (0-100)', '80')
  .option('--types <types...>', 'Fix types to apply')
  .option('-i, --interactive', 'Interactive mode')
  .action(fixCommand)

// Check command (for CI)
program
  .command('check [path]')
  .description('Check code quality (CI mode)')
  .option('--threshold <severity>', 'Fail on severity threshold', 'error')
  .option('--format <format>', 'Output format (junit, github)', 'text')
  .action(checkCommand)

// Init command
program
  .command('init')
  .description('Initialize CPPCheck Studio configuration')
  .action(initCommand)

// Custom error handling
program.on('command:*', () => {
  console.error(chalk.red('Invalid command: %s'), program.args.join(' '))
  console.log('See --help for a list of available commands.')
  process.exit(1)
})

// Parse arguments
program.parse(process.argv)

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp()
}