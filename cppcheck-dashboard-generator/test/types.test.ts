import { Issue, Stats, DashboardConfig } from '../src/types';

describe('Type definitions', () => {
  describe('Issue type', () => {
    it('should allow valid issue objects', () => {
      const validIssue: Issue = {
        file: 'test.cpp',
        line: 42,
        severity: 'error',
        message: 'Test error',
        id: 'TEST001',
      };
      expect(validIssue).toBeDefined();
    });

    it('should allow issues with code context', () => {
      const issueWithContext: Issue = {
        file: 'test.cpp',
        line: '42', // string also allowed
        severity: 'warning',
        message: 'Test warning',
        code_context: {
          lines: [
            { number: 41, content: 'int x = 0;' },
            { number: 42, content: 'return x;', is_target: true },
          ],
        },
      };
      expect(issueWithContext.code_context).toBeDefined();
    });

    it('should allow additional properties', () => {
      const issueWithExtra: Issue = {
        file: 'test.cpp',
        customField: 'custom value', // Additional properties allowed
        anotherField: 123,
      };
      expect(issueWithExtra.customField).toBe('custom value');
    });
  });

  describe('Stats type', () => {
    it('should have all required properties', () => {
      const stats: Stats = {
        total: 100,
        errors: 25,
        warnings: 30,
        style: 40,
        performance: 5,
        information: 0,
        error_percent: 25,
        warning_percent: 30,
        style_percent: 40,
        performance_percent: 5,
      };

      expect(Object.keys(stats)).toHaveLength(10);
    });
  });

  describe('DashboardConfig type', () => {
    it('should have all configuration properties', () => {
      const config: DashboardConfig = {
        ROW_HEIGHT: 50,
        VISIBLE_BUFFER: 5,
        SCROLL_DEBOUNCE: 10,
        SEARCH_DEBOUNCE: 300,
        BATCH_SIZE: 50,
      };

      expect(config.ROW_HEIGHT).toBe(50);
      expect(config.VISIBLE_BUFFER).toBe(5);
    });
  });

  describe('Severity type', () => {
    it('should accept valid severity values', () => {
      const severities = [
        'error',
        'warning',
        'style',
        'performance',
        'information',
        'portability',
        'none',
      ];

      severities.forEach(severity => {
        const issue: Issue = { severity };
        expect(issue.severity).toBe(severity);
      });
    });
  });
});
