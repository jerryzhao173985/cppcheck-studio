import { StandaloneVirtualDashboardGenerator } from '../src';

// Basic usage example
async function generateBasicDashboard() {
  console.log('Generating basic dashboard...');
  
  const generator = new StandaloneVirtualDashboardGenerator({
    input: '../data/analysis-with-context.json',
    output: 'basic-dashboard.html',
    verbose: true
  });

  try {
    await generator.generate();
    console.log('Dashboard generated successfully!');
  } catch (error) {
    console.error('Failed to generate dashboard:', error);
  }
}

// Run the example
generateBasicDashboard();