/**
 * CPPCheck Dashboard Generator
 *
 * A TypeScript library for generating beautiful, interactive HTML dashboards
 * from cppcheck JSON output with virtual scrolling support.
 *
 * @packageDocumentation
 */

// Main class export
export { StandaloneVirtualDashboardGenerator } from './generator';
export { StandaloneVirtualDashboardGenerator as DashboardGenerator } from './generator';
export { StandaloneVirtualDashboardGenerator as default } from './generator';

// Type exports
export type {
  // Core types
  Issue,
  CodeContext,
  CodeLine,
  AnalysisData,
  Stats,
  Severity,

  // Configuration types
  GeneratorOptions,
  GeneratorResult,
  DashboardConfig,
  APIOptions,

  // State types
  FilterState,
  ScrollState,
} from './types';

// Re-export all types as namespace for convenience
export * as Types from './types';

// Utility exports for advanced usage
export { generateStyles } from './styles';
export { generateScripts } from './scripts';

// Version information
export const VERSION = '1.0.0';

// Default configuration
export const DEFAULT_CONFIG: Partial<import('./types').DashboardConfig> = {
  ROW_HEIGHT: 50,
  VISIBLE_BUFFER: 5,
  SCROLL_DEBOUNCE: 10,
  SEARCH_DEBOUNCE: 300,
  BATCH_SIZE: 50,
};

/**
 * Quick start example:
 * ```typescript
 * import { StandaloneVirtualDashboardGenerator } from 'cppcheck-dashboard-generator';
 *
 * const generator = new StandaloneVirtualDashboardGenerator({
 *   input: 'analysis.json',
 *   output: 'dashboard.html',
 *   title: 'My Project Analysis',
 *   projectName: 'MyProject'
 * });
 *
 * await generator.generate();
 * ```
 *
 * Advanced usage with custom configuration:
 * ```typescript
 * import { DashboardGenerator, Types } from 'cppcheck-dashboard-generator';
 *
 * const config: Partial<Types.DashboardConfig> = {
 *   ROW_HEIGHT: 60,
 *   VISIBLE_BUFFER: 10
 * };
 *
 * const generator = new DashboardGenerator({
 *   input: 'analysis.json',
 *   output: 'custom-dashboard.html',
 *   config,
 *   verbose: true  // Will print statistics to console
 * });
 *
 * await generator.generate();
 * console.log('Dashboard generated successfully!');
 * ```
 */
