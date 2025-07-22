import { StandaloneVirtualDashboardGenerator } from '../src/generator';
import { AnalysisData, Issue, GeneratorOptions } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';

// Mock fs module
jest.mock('fs');
const mockFs = fs as jest.Mocked<typeof fs>;

// Mock fs.promises
mockFs.promises = {
  readFile: jest.fn(),
  writeFile: jest.fn(),
  stat: jest.fn(),
} as any;

// Mock crypto for consistent IDs
jest.mock('crypto', () => ({
  createHash: jest.fn(() => ({
    update: jest.fn().mockReturnThis(),
    digest: jest.fn(() => 'mockedHash123'),
  })),
}));

describe('StandaloneVirtualDashboardGenerator', () => {
  const mockAnalysisData: AnalysisData = {
    issues: [
      {
        file: 'test.cpp',
        line: 10,
        severity: 'error',
        message: 'Test error message',
        id: 'testError',
      },
      {
        file: 'test2.cpp',
        line: 20,
        severity: 'warning',
        message: 'Test warning message',
        id: 'testWarning',
        code_context: {
          lines: [
            { number: 19, content: 'void test() {' },
            { number: 20, content: '  int x;', is_target: true },
            { number: 21, content: '}' },
          ],
        },
      },
    ],
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockFs.existsSync.mockReturnValue(true);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(mockAnalysisData));
    mockFs.writeFileSync.mockImplementation(() => {});
    (mockFs.promises.readFile as jest.Mock).mockResolvedValue(JSON.stringify(mockAnalysisData));
    (mockFs.promises.writeFile as jest.Mock).mockResolvedValue(undefined);
    (mockFs.promises.stat as jest.Mock).mockResolvedValue({ size: 1000000 });
  });

  describe('constructor', () => {
    it('should create instance with required options', () => {
      const options: GeneratorOptions = {
        input: 'input.json',
        output: 'output.html',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      expect(generator).toBeDefined();
    });

    it('should use default output path if not provided', () => {
      const options: GeneratorOptions = {
        input: 'input.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      expect(generator).toBeDefined();
    });

    it('should merge custom config with defaults', () => {
      const options: GeneratorOptions = {
        input: 'input.json',
        config: {
          ROW_HEIGHT: 60,
          VISIBLE_BUFFER: 10,
        },
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      expect(generator).toBeDefined();
    });
  });

  describe('generate', () => {
    it('should generate dashboard successfully', async () => {
      const options: GeneratorOptions = {
        input: 'test.json',
        output: 'test-output.html',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      expect(mockFs.promises.readFile).toHaveBeenCalledWith('test.json', 'utf-8');
      expect(mockFs.promises.writeFile).toHaveBeenCalledWith(
        'test-output.html',
        expect.stringContaining('<!DOCTYPE html>'),
        'utf-8'
      );
    });

    it('should handle file not found error', async () => {
      mockFs.existsSync.mockReturnValue(false);
      const options: GeneratorOptions = {
        input: 'nonexistent.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);

      await expect(generator.generate()).rejects.toThrow('Input file not found');
    });

    it('should handle invalid JSON', async () => {
      (mockFs.promises.readFile as jest.Mock).mockResolvedValue('invalid json');
      const options: GeneratorOptions = {
        input: 'invalid.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);

      await expect(generator.generate()).rejects.toThrow();
    });

    it('should generate unique IDs for issues without them', async () => {
      const dataWithoutIds: AnalysisData = {
        issues: [
          {
            file: 'test.cpp',
            line: 10,
            severity: 'error',
            message: 'Error without ID',
          },
        ],
      };
      (mockFs.promises.readFile as jest.Mock).mockResolvedValue(JSON.stringify(dataWithoutIds));

      const options: GeneratorOptions = {
        input: 'test.json',
        output: 'test-output.html',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      expect(crypto.createHash).toHaveBeenCalled();
    });
  });

  describe('calculateStats', () => {
    it('should calculate correct statistics', async () => {
      const options: GeneratorOptions = {
        input: 'test.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      const generatedHtml = (mockFs.promises.writeFile as jest.Mock).mock.calls[0][1] as string;
      expect(generatedHtml).toContain('"total": 2');
      expect(generatedHtml).toContain('"errors": 1');
      expect(generatedHtml).toContain('"warnings": 1');
    });

    it('should handle empty issues array', async () => {
      (mockFs.promises.readFile as jest.Mock).mockResolvedValue(JSON.stringify({ issues: [] }));
      const options: GeneratorOptions = {
        input: 'empty.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      const generatedHtml = (mockFs.promises.writeFile as jest.Mock).mock.calls[0][1] as string;
      expect(generatedHtml).toContain('"total": 0');
    });
  });

  describe('data embedding', () => {
    it('should embed issues as JSONL', async () => {
      const options: GeneratorOptions = {
        input: 'test.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      const generatedHtml = (mockFs.promises.writeFile as jest.Mock).mock.calls[0][1] as string;
      expect(generatedHtml).toContain('<script id="issuesData" type="application/x-ndjson">');
      expect(generatedHtml).toMatch(/\{"file":"test\.cpp".*\}\n\{"file":"test2\.cpp".*\}/);
    });

    it('should separate code context', async () => {
      const options: GeneratorOptions = {
        input: 'test.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      const generatedHtml = (mockFs.promises.writeFile as jest.Mock).mock.calls[0][1] as string;
      expect(generatedHtml).toContain('<script id="codeContextData" type="application/x-ndjson">');
      expect(generatedHtml).toContain('"code_context":{"lines"');
    });
  });

  describe('HTML generation', () => {
    it('should include custom title', async () => {
      const options: GeneratorOptions = {
        input: 'test.json',
        title: 'Custom Dashboard Title',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      const generatedHtml = (mockFs.promises.writeFile as jest.Mock).mock.calls[0][1] as string;
      expect(generatedHtml).toContain('<title>Custom Dashboard Title</title>');
    });

    it('should include project name', async () => {
      const options: GeneratorOptions = {
        input: 'test.json',
        projectName: 'My Awesome Project',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      const generatedHtml = (mockFs.promises.writeFile as jest.Mock).mock.calls[0][1] as string;
      expect(generatedHtml).toContain('My Awesome Project');
    });

    it('should include all required scripts', async () => {
      const options: GeneratorOptions = {
        input: 'test.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      const generatedHtml = (mockFs.promises.writeFile as jest.Mock).mock.calls[0][1] as string;
      expect(generatedHtml).toContain('function initVirtualScroll()');
      expect(generatedHtml).toContain('function renderVisibleRows()');
      expect(generatedHtml).toContain('function filterIssues()');
    });

    it('should include all required styles', async () => {
      const options: GeneratorOptions = {
        input: 'test.json',
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      const generatedHtml = (mockFs.promises.writeFile as jest.Mock).mock.calls[0][1] as string;
      expect(generatedHtml).toContain('<style>');
      expect(generatedHtml).toContain('.dashboard-container');
      expect(generatedHtml).toContain('.virtual-scroll-container');
    });
  });

  describe('verbose logging', () => {
    it('should log when verbose is enabled', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      const options: GeneratorOptions = {
        input: 'test.json',
        verbose: true,
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Loading analysis data'));
      consoleSpy.mockRestore();
    });

    it('should not log when verbose is disabled', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      const options: GeneratorOptions = {
        input: 'test.json',
        verbose: false,
      };
      const generator = new StandaloneVirtualDashboardGenerator(options);
      await generator.generate();

      expect(consoleSpy).not.toHaveBeenCalled();
      consoleSpy.mockRestore();
    });
  });
});
