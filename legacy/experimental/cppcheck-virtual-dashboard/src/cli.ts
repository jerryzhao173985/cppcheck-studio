#!/usr/bin/env node

import { program } from 'commander';
import * as path from 'path';
import * as fs from 'fs';
import { VirtualDashboardGenerator } from './generator';

program
  .name('cppcheck-dashboard')
  .description('Generate standalone virtual scroll dashboards for CPPCheck analysis results')
  .version('1.0.0')
  .argument('<input>', 'Input JSON file containing CPPCheck analysis results')
  .argument('[output]', 'Output HTML file (default: virtual-dashboard.html)')
  .option('-t, --title <title>', 'Dashboard title', 'CPPCheck Studio - Virtual Scroll Dashboard')
  .option('-p, --project <name>', 'Project name', 'Project')
  .action((input: string, output?: string) => {
    try {
      // Validate input file exists
      if (!fs.existsSync(input)) {
        console.error(`❌ Error: Input file '${input}' not found`);
        process.exit(1);
      }

      // Determine output file
      const outputFile = output || 'virtual-dashboard.html';

      // Create generator with options
      const generator = new VirtualDashboardGenerator(input, {
        title: program.opts().title,
        projectName: program.opts().project
      });

      // Generate dashboard
      generator.generate(outputFile);

    } catch (error) {
      console.error('❌ Error:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

program.parse();