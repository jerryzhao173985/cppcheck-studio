import { generateStyles } from '../src/styles';
import { generateScripts } from '../src/scripts';

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
  it('should generate valid JavaScript', () => {
    const scripts = generateScripts();
    expect(scripts).toContain('function');
    expect(scripts).toContain('const');
    expect(scripts).toContain('let');
  });

  it('should include all required functions', () => {
    const scripts = generateScripts();

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
    const scripts = generateScripts();
    // Check for default configuration values
    expect(scripts).toContain('ROW_HEIGHT');
    expect(scripts).toContain('VISIBLE_BUFFER');
    expect(scripts).toContain('SCROLL_DEBOUNCE');
    expect(scripts).toContain('SEARCH_DEBOUNCE');
    expect(scripts).toContain('BATCH_SIZE');
  });

  it('should include state management', () => {
    const scripts = generateScripts();
    expect(scripts).toContain('const state = {');
    expect(scripts).toContain('allIssues: []');
    expect(scripts).toContain('filteredIssues: []');
    expect(scripts).toContain('codeContextMap: new Map()');
    expect(scripts).toContain('currentFilter:');
    expect(scripts).toContain('currentSearch:');
  });

  it('should include event listeners setup', () => {
    const scripts = generateScripts();
    expect(scripts).toContain('addEventListener(');
    expect(scripts).toContain("querySelector('.search-input')");
    expect(scripts).toContain("querySelector('.scroll-container')");
    expect(scripts).toContain("querySelectorAll('.severity-filter')");
  });

  it('should include DOMContentLoaded handler', () => {
    const scripts = generateScripts();
    expect(scripts).toContain("document.addEventListener('DOMContentLoaded'");
    expect(scripts).toContain('initVirtualScroll()');
  });

  it('should handle JSONL parsing', () => {
    const scripts = generateScripts();
    expect(scripts).toContain(".split('\\n')");
    expect(scripts).toContain('JSON.parse(');
    expect(scripts).toContain('.filter(line => line.trim())');
  });
});
