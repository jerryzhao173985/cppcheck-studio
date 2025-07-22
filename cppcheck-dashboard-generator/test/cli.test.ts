import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

describe('CLI Integration Tests', () => {
  const cliPath = path.join(__dirname, '../dist/cli.js');
  const testDataPath = path.join(__dirname, '../test-data.json');
  const outputPath = path.join(__dirname, '../test-output-cli.html');

  beforeAll(() => {
    // Ensure the CLI is built
    execSync('npm run build', { cwd: path.join(__dirname, '..') });
  });

  afterEach(() => {
    // Clean up test output
    if (fs.existsSync(outputPath)) {
      fs.unlinkSync(outputPath);
    }
  });

  describe('command execution', () => {
    it('should show help when no arguments provided', () => {
      const result = execSync(`node ${cliPath} --help`).toString();
      expect(result).toContain('Usage:');
      expect(result).toContain('Generate beautiful');
      expect(result).toContain('Options:');
    });

    it('should show version', () => {
      const result = execSync(`node ${cliPath} --version`).toString();
      expect(result).toMatch(/\d+\.\d+\.\d+/);
    });

    it('should generate dashboard with minimal arguments', () => {
      execSync(`node ${cliPath} ${testDataPath} ${outputPath}`);
      expect(fs.existsSync(outputPath)).toBe(true);

      const content = fs.readFileSync(outputPath, 'utf-8');
      expect(content).toContain('<!DOCTYPE html>');
      expect(content).toContain('<script id="issuesData"');
    });

    it('should generate dashboard with custom title', () => {
      execSync(`node ${cliPath} ${testDataPath} ${outputPath} --title "Test Dashboard"`);

      const content = fs.readFileSync(outputPath, 'utf-8');
      expect(content).toContain('<title>Test Dashboard</title>');
    });

    it('should generate dashboard with project name', () => {
      execSync(`node ${cliPath} ${testDataPath} ${outputPath} --project "TestProject"`);

      const content = fs.readFileSync(outputPath, 'utf-8');
      expect(content).toContain('TestProject');
    });

    it('should handle verbose mode', () => {
      const result = execSync(`node ${cliPath} ${testDataPath} ${outputPath} --verbose`).toString();

      expect(result).toContain('Loading analysis data');
      expect(result).toContain('Generating dashboard');
      expect(result).toContain('Dashboard generated successfully');
    });

    it('should handle missing input file gracefully', () => {
      expect(() => {
        execSync(`node ${cliPath} nonexistent.json ${outputPath}`);
      }).toThrow();
    });

    it('should use default output filename when not specified', () => {
      const defaultOutput = 'cppcheck-dashboard.html';
      execSync(`node ${cliPath} ${testDataPath}`);

      expect(fs.existsSync(defaultOutput)).toBe(true);
      fs.unlinkSync(defaultOutput);
    });
  });

  describe('error handling', () => {
    it('should show error for invalid JSON', () => {
      const invalidJsonPath = path.join(__dirname, 'invalid.json');
      fs.writeFileSync(invalidJsonPath, 'not json');

      expect(() => {
        execSync(`node ${cliPath} ${invalidJsonPath} ${outputPath}`);
      }).toThrow();

      fs.unlinkSync(invalidJsonPath);
    });

    it('should show error for empty file', () => {
      const emptyPath = path.join(__dirname, 'empty.json');
      fs.writeFileSync(emptyPath, '');

      expect(() => {
        execSync(`node ${cliPath} ${emptyPath} ${outputPath}`);
      }).toThrow();

      fs.unlinkSync(emptyPath);
    });
  });
});
