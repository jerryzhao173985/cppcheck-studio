#!/usr/bin/env node
/* eslint-disable no-console */

import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import chalk from 'chalk';
import { StandaloneVirtualDashboardGenerator } from './generator';
import { GeneratorOptions } from './types';

const program = new Command();

program
  .name('cppcheck-dashboard')
  .description('Generate beautiful, interactive HTML dashboards from cppcheck JSON output')
  .version('1.0.0')
  .argument('<input>', 'cppcheck JSON analysis file')
  .argument('[output]', 'output HTML file (default: standalone-virtual-dashboard.html)')
  .option('-t, --title <title>', 'dashboard title', 'CPPCheck Studio - Virtual Scroll Dashboard')
  .option('-p, --project <name>', 'project name', 'Project')
  .option('-v, --verbose', 'enable verbose output', false)
  .action(
    async (
      input: string,
      output: string | undefined,
      options: { title: string; project: string; verbose: boolean }
    ) => {
      try {
        // Validate input file exists
        if (!fs.existsSync(input)) {
          console.error(chalk.red(`Error: Input file '${input}' not found`));
          process.exit(1);
        }

        // Determine output file
        const outputFile = output || 'standalone-virtual-dashboard.html';

        // Show banner
        console.log(chalk.cyan('\n╔══════════════════════════════════════════╗'));
        console.log(chalk.cyan('║     CPPCheck Dashboard Generator         ║'));
        console.log(chalk.cyan('╚══════════════════════════════════════════╝\n'));

        // Show configuration
        console.log(chalk.gray('Configuration:'));
        console.log(chalk.gray(`  Input:   ${input}`));
        console.log(chalk.gray(`  Output:  ${outputFile}`));
        console.log(chalk.gray(`  Title:   ${options.title}`));
        console.log(chalk.gray(`  Project: ${options.project}\n`));

        // Create generator options
        const generatorOptions: GeneratorOptions = {
          input,
          output: outputFile,
          title: options.title,
          projectName: options.project,
          verbose: options.verbose,
        };

        // Generate dashboard
        const generator = new StandaloneVirtualDashboardGenerator(generatorOptions);
        await generator.generate();

        // Show success message
        console.log(chalk.green('\n✨ Dashboard generated successfully!'));
        console.log(chalk.gray(`\nOpen in browser:`));
        console.log(chalk.cyan(`  file://${path.resolve(outputFile)}\n`));
      } catch (error) {
        console.error(
          chalk.red('\n❌ Error:'),
          error instanceof Error ? error.message : String(error)
        );
        process.exit(1);
      }
    }
  );

// Parse command line arguments
program.parse(process.argv);

// Show help if no arguments provided
if (process.argv.length < 3) {
  program.help();
}
