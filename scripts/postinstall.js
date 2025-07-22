#!/usr/bin/env node
/**
 * Post-install script for CPPCheck Studio
 * Checks dependencies and provides helpful messages
 */

const { execSync } = require('child_process');
const os = require('os');

// Colors
const colors = {
  red: '\x1b[0;31m',
  green: '\x1b[0;32m',
  yellow: '\x1b[1;33m',
  blue: '\x1b[0;34m',
  nc: '\x1b[0m'
};

console.log(`${colors.blue}
╔═══════════════════════════════════════════╗
║     CPPCheck Studio Post-Install Check    ║
╚═══════════════════════════════════════════╝
${colors.nc}`);

// Check Python
try {
  const pythonVersion = execSync('python3 --version').toString().trim();
  console.log(`${colors.green}✓${colors.nc} ${pythonVersion}`);
} catch (e) {
  console.log(`${colors.red}✗${colors.nc} Python 3 not found!`);
  console.log('  Please install Python 3.6 or higher');
  process.exit(1);
}

// Check cppcheck
try {
  const cppcheckVersion = execSync('cppcheck --version').toString().trim();
  console.log(`${colors.green}✓${colors.nc} ${cppcheckVersion}`);
} catch (e) {
  console.log(`${colors.yellow}⚠${colors.nc} cppcheck not found`);
  console.log('  To install cppcheck:');
  
  const platform = os.platform();
  if (platform === 'darwin') {
    console.log('    brew install cppcheck');
  } else if (platform === 'linux') {
    console.log('    sudo apt-get install cppcheck  # Ubuntu/Debian');
    console.log('    sudo yum install cppcheck       # RedHat/CentOS');
  }
}

console.log(`
${colors.green}Installation complete!${colors.nc}

To get started:
  npx cppcheck-studio init      # Initialize project
  npx cppcheck-studio analyze   # Run analysis
  npx cppcheck-studio serve     # View dashboard

For help:
  npx cppcheck-studio --help
`);

// Make executable
try {
  execSync('chmod +x bin/cppcheck-studio');
} catch (e) {
  // Ignore on Windows
}