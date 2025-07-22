import { generateStyles } from '../src/styles';
import { generateScripts } from '../src/scripts';
import { DashboardConfig } from '../src/types';

describe('generateStyles', () => {
  it('should generate valid CSS', () => {
    const styles = generateStyles();
    expect(styles).toContain('body');
    expect(styles).toContain('.dashboard-container');
    expect(styles).toContain('.virtual-scroll-container');
    expect(styles).toContain('.stat-card');
  });

  it('should include all required component styles', () => {
    const styles = generateStyles();

    // Check for main layout components
    expect(styles).toContain('.header');
    expect(styles).toContain('.content');
    expect(styles).toContain('.filters');
    expect(styles).toContain('.stats');

    // Check for table styles
    expect(styles).toContain('.issues-table');
    expect(styles).toContain('th');
    expect(styles).toContain('td');

    // Check for interactive elements
    expect(styles).toContain('.severity-filter');
    expect(styles).toContain('.search-input');
    expect(styles).toContain('.modal');

    // Check for responsive styles
    expect(styles).toContain('@media');
  });

  it('should include virtual scroll specific styles', () => {
    const styles = generateStyles();
    expect(styles).toContain('.scroll-container');
    expect(styles).toContain('.spacer');
    expect(styles).toContain('.virtual-row');
  });

  it('should include severity colors', () => {
    const styles = generateStyles();
    expect(styles).toContain('.severity-error');
    expect(styles).toContain('.severity-warning');
    expect(styles).toContain('.severity-style');
    expect(styles).toContain('.severity-performance');
  });
});

describe('generateScripts', () => {
  const defaultConfig: DashboardConfig = {
    ROW_HEIGHT: 50,
    VISIBLE_BUFFER: 5,
    SCROLL_DEBOUNCE: 10,
    SEARCH_DEBOUNCE: 300,
    BATCH_SIZE: 50,
  };

  it('should generate valid JavaScript', () => {
    const scripts = generateScripts(defaultConfig);
    expect(scripts).toContain('function');
    expect(scripts).toContain('const');
    expect(scripts).toContain('let');
  });

  it('should include all required functions', () => {
    const scripts = generateScripts(defaultConfig);

    // Core functions
    expect(scripts).toContain('function initVirtualScroll()');
    expect(scripts).toContain('function renderVisibleRows()');
    expect(scripts).toContain('function filterIssues()');
    expect(scripts).toContain('function debounce(');

    // Data loading functions
    expect(scripts).toContain('function loadIssuesData()');
    expect(scripts).toContain('function loadCodeContextData()');

    // UI functions
    expect(scripts).toContain('function showCodeModal(');
    expect(scripts).toContain('function closeCodeModal()');
    expect(scripts).toContain('function handleScroll()');
    expect(scripts).toContain('function handleSearch(');
    expect(scripts).toContain('function handleFilterClick(');
  });

  it('should include configuration values', () => {
    const customConfig: DashboardConfig = {
      ROW_HEIGHT: 60,
      VISIBLE_BUFFER: 10,
      SCROLL_DEBOUNCE: 20,
      SEARCH_DEBOUNCE: 500,
      BATCH_SIZE: 100,
    };

    const scripts = generateScripts(customConfig);
    expect(scripts).toContain('ROW_HEIGHT = 60');
    expect(scripts).toContain('VISIBLE_BUFFER = 10');
    expect(scripts).toContain('SCROLL_DEBOUNCE = 20');
    expect(scripts).toContain('SEARCH_DEBOUNCE = 500');
    expect(scripts).toContain('BATCH_SIZE = 100');
  });

  it('should include state management', () => {
    const scripts = generateScripts(defaultConfig);
    expect(scripts).toContain('const state = {');
    expect(scripts).toContain('allIssues: []');
    expect(scripts).toContain('filteredIssues: []');
    expect(scripts).toContain('codeContextMap: new Map()');
    expect(scripts).toContain('currentFilter:');
    expect(scripts).toContain('currentSearch:');
  });

  it('should include event listeners setup', () => {
    const scripts = generateScripts(defaultConfig);
    expect(scripts).toContain('addEventListener(');
    expect(scripts).toContain("querySelector('.search-input')");
    expect(scripts).toContain("querySelector('.scroll-container')");
    expect(scripts).toContain("querySelectorAll('.severity-filter')");
  });

  it('should include DOMContentLoaded handler', () => {
    const scripts = generateScripts(defaultConfig);
    expect(scripts).toContain("document.addEventListener('DOMContentLoaded'");
    expect(scripts).toContain('initVirtualScroll()');
  });

  it('should handle JSONL parsing', () => {
    const scripts = generateScripts(defaultConfig);
    expect(scripts).toContain(".split('\\n')");
    expect(scripts).toContain('JSON.parse(');
    expect(scripts).toContain('.filter(line => line.trim())');
  });
});
