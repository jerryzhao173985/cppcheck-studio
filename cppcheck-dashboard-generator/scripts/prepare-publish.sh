#!/bin/bash

# Script to prepare the package for npm publishing

echo "🚀 Preparing cppcheck-dashboard-generator for npm publishing..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the package root."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
npm run clean

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Run validation (lint, typecheck, tests)
echo "✅ Running validation..."
npm run validate

if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Please fix the issues before publishing."
    exit 1
fi

# Build the package
echo "🔨 Building package..."
npm run build

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "❌ Build failed: dist directory not found."
    exit 1
fi

# Check if all required files exist
required_files=("README.md" "LICENSE" "package.json" "bin/cppcheck-dashboard")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Required file $file not found."
        exit 1
    fi
done

# Run a dry-run to see what will be published
echo "📋 Files that will be published:"
npm pack --dry-run

echo ""
echo "✨ Package is ready for publishing!"
echo ""
echo "To publish to npm:"
echo "  1. Make sure you're logged in: npm login"
echo "  2. Publish with: npm publish"
echo ""
echo "To test locally first:"
echo "  1. Create a tarball: npm pack"
echo "  2. Install in another project: npm install /path/to/cppcheck-dashboard-generator-1.0.0.tgz"
echo ""
echo "Current version: $(node -p "require('./package.json').version")"
echo "Don't forget to update the version before publishing!"
echo "  - Patch release: npm version patch"
echo "  - Minor release: npm version minor"
echo "  - Major release: npm version major"