import { 
  StandaloneVirtualDashboardGenerator,
  type GeneratorOptions,
  type DashboardConfig 
} from '../src';

// Advanced usage example with custom configuration
async function generateAdvancedDashboard() {
  console.log('Generating advanced dashboard with custom config...');
  
  // Custom dashboard configuration
  const customConfig: Partial<DashboardConfig> = {
    ROW_HEIGHT: 60,          // Taller rows for better readability
    VISIBLE_BUFFER: 10,      // More rows rendered outside viewport
    SCROLL_DEBOUNCE: 5,      // Faster scroll response
    SEARCH_DEBOUNCE: 200,    // Faster search response
    BATCH_SIZE: 200          // Process more items at once
  };

  const options: GeneratorOptions = {
    input: '../data/analysis-with-context.json',
    output: 'advanced-dashboard.html',
    title: 'Advanced Code Analysis Dashboard',
    projectName: 'My Large C++ Project',
    config: customConfig,
    verbose: true
  };

  const generator = new StandaloneVirtualDashboardGenerator(options);

  try {
    // Generate the dashboard
    await generator.generate();
    console.log('Advanced dashboard generated successfully!');
    
    // You can also access the data programmatically
    const analysisData = await generator.loadAnalysisData();
    console.log(`Total issues found: ${analysisData.issues.length}`);
    
    // Calculate statistics
    const stats = generator.calculateStats();
    console.log('Statistics:', {
      total: stats.total,
      errors: stats.errors,
      warnings: stats.warnings
    });
    
  } catch (error) {
    console.error('Failed to generate dashboard:', error);
  }
}

// Example: Generate multiple dashboards with different configurations
async function generateMultipleDashboards() {
  const configurations = [
    {
      name: 'minimal',
      config: { ROW_HEIGHT: 40, VISIBLE_BUFFER: 3 }
    },
    {
      name: 'performance',
      config: { BATCH_SIZE: 500, SCROLL_DEBOUNCE: 0 }
    },
    {
      name: 'detailed',
      config: { ROW_HEIGHT: 80, VISIBLE_BUFFER: 15 }
    }
  ];

  for (const { name, config } of configurations) {
    const generator = new StandaloneVirtualDashboardGenerator({
      input: '../data/analysis-with-context.json',
      output: `dashboard-${name}.html`,
      title: `${name.charAt(0).toUpperCase() + name.slice(1)} Dashboard`,
      config,
      verbose: false
    });

    try {
      await generator.generate();
      console.log(`Generated ${name} dashboard`);
    } catch (error) {
      console.error(`Failed to generate ${name} dashboard:`, error);
    }
  }
}

// Run the examples
async function main() {
  await generateAdvancedDashboard();
  console.log('\n---\n');
  await generateMultipleDashboards();
}

main();