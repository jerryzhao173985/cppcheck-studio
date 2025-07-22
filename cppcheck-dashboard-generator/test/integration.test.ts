import { StandaloneVirtualDashboardGenerator } from '../src/generator';
import { AnalysisData } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

// Integration tests that test the full workflow
describe('Integration Tests', () => {
  const testDataDir = path.join(__dirname, 'test-data');
  const outputDir = path.join(__dirname, 'test-output');

  beforeAll(() => {
    // Create test directories
    if (!fs.existsSync(testDataDir)) {
      fs.mkdirSync(testDataDir, { recursive: true });
    }
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
  });

  afterAll(() => {
    // Cleanup test output
    if (fs.existsSync(outputDir)) {
      fs.rmSync(outputDir, { recursive: true, force: true });
    }
  });

  describe('CLI Integration', () => {
    const cliPath = path.join(__dirname, '../dist/cli.js');

    beforeAll(() => {
      // Build the project
      execSync('npm run build', { cwd: path.join(__dirname, '..') });
    });

    it('should show help when --help is passed', () => {
      const output = execSync(`node ${cliPath} --help`).toString();
      expect(output).toContain('Usage: cppcheck-dashboard');
      expect(output).toContain('--title');
      expect(output).toContain('--project-name');
      expect(output).toContain('--verbose');
    });

    it('should generate dashboard from CLI', () => {
      // Create test data
      const testData: AnalysisData = {
        issues: [
          {
            file: 'test.cpp',
            line: 10,
            severity: 'error',
            message: 'Test error',
            id: 'TEST001',
          },
        ],
      };

      const inputFile = path.join(testDataDir, 'cli-test.json');
      const outputFile = path.join(outputDir, 'cli-output.html');

      fs.writeFileSync(inputFile, JSON.stringify(testData));

      // Run CLI
      execSync(`node ${cliPath} ${inputFile} ${outputFile} --title "CLI Test"`);

      // Verify output
      expect(fs.existsSync(outputFile)).toBe(true);
      const html = fs.readFileSync(outputFile, 'utf-8');
      expect(html).toContain('CLI Test');
      expect(html).toContain('TEST001');
    });
  });

  describe('Programmatic API Integration', () => {
    it('should generate dashboard with real-world data structure', async () => {
      // Create realistic test data
      const testData: AnalysisData = {
        issues: [
          {
            file: '/src/main.cpp',
            line: 42,
            severity: 'error',
            message: 'Memory leak: buffer',
            id: 'memleak',
            code_context: {
              lines: [
                { number: 41, content: 'char* buffer = new char[256];' },
                { number: 42, content: 'return 0;', is_target: true },
                { number: 43, content: '}' },
              ],
            },
          },
          {
            file: '/src/utils.cpp',
            line: 100,
            severity: 'warning',
            message: 'Variable is assigned a value that is never used',
            id: 'unreadVariable',
          },
          {
            file: '/src/config.cpp',
            line: 25,
            severity: 'style',
            message: 'The scope of the variable can be reduced',
            id: 'variableScope',
          },
        ],
      };

      const inputFile = path.join(testDataDir, 'api-test.json');
      const outputFile = path.join(outputDir, 'api-output.html');

      fs.writeFileSync(inputFile, JSON.stringify(testData));

      const generator = new StandaloneVirtualDashboardGenerator({
        input: inputFile,
        output: outputFile,
        title: 'Integration Test Dashboard',
        projectName: 'Test Project',
        verbose: false,
      });

      await generator.generate();

      // Verify output
      expect(fs.existsSync(outputFile)).toBe(true);
      const html = fs.readFileSync(outputFile, 'utf-8');

      // Check statistics
      expect(html).toContain('"total": 3');
      expect(html).toContain('"errors": 1');
      expect(html).toContain('"warnings": 1');
      expect(html).toContain('"style": 1');

      // Check JSONL data
      expect(html).toContain('type="application/x-ndjson"');
      expect(html).toContain('memleak');
      expect(html).toContain('unreadVariable');
      expect(html).toContain('variableScope');

      // Check code context
      expect(html).toContain('char* buffer = new char[256];');
    });

    it('should handle large datasets efficiently', async () => {
      // Generate large dataset
      const issues = [];
      for (let i = 0; i < 10000; i++) {
        issues.push({
          file: `/src/file${i % 100}.cpp`,
          line: i,
          severity: ['error', 'warning', 'style'][i % 3],
          message: `Issue ${i}`,
          id: `ISSUE${i}`,
        });
      }

      const testData: AnalysisData = { issues };
      const inputFile = path.join(testDataDir, 'large-test.json');
      const outputFile = path.join(outputDir, 'large-output.html');

      fs.writeFileSync(inputFile, JSON.stringify(testData));

      const generator = new StandaloneVirtualDashboardGenerator({
        input: inputFile,
        output: outputFile,
        verbose: false,
      });

      const startTime = Date.now();
      await generator.generate();
      const endTime = Date.now();

      // Should complete in reasonable time
      expect(endTime - startTime).toBeLessThan(5000); // 5 seconds

      // Verify output
      expect(fs.existsSync(outputFile)).toBe(true);
      const stats = fs.statSync(outputFile);
      expect(stats.size).toBeGreaterThan(1000000); // At least 1MB
    });
  });

  describe('Error Handling Integration', () => {
    it('should handle missing input file gracefully', async () => {
      const generator = new StandaloneVirtualDashboardGenerator({
        input: '/nonexistent/file.json',
        output: path.join(outputDir, 'error.html'),
      });

      await expect(generator.generate()).rejects.toThrow('Input file not found');
    });

    it('should handle corrupted JSON gracefully', async () => {
      const inputFile = path.join(testDataDir, 'corrupted.json');
      fs.writeFileSync(inputFile, '{ invalid json }');

      const generator = new StandaloneVirtualDashboardGenerator({
        input: inputFile,
        output: path.join(outputDir, 'corrupted.html'),
      });

      await expect(generator.generate()).rejects.toThrow();
    });
  });
});
