#!/bin/bash

set -e

echo "🚀 Building CPPCheck Studio..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build packages in order
echo "🔧 Building core package..."
npm run build --workspace=@cppcheck-studio/core

echo "🎨 Building UI package..."
npm run build --workspace=@cppcheck-studio/ui

echo "💻 Building CLI package..."
npm run build --workspace=cppcheck-studio

echo "🌐 Building web app..."
npm run build --workspace=@cppcheck-studio/web

echo "🔌 Building API server..."
npm run build --workspace=@cppcheck-studio/api

echo "✅ Build complete!"

# Optional: Run tests
if [ "$1" = "--test" ]; then
  echo "🧪 Running tests..."
  npm test
fi

# Optional: Create production bundle
if [ "$1" = "--prod" ]; then
  echo "📦 Creating production bundle..."
  
  # Create dist directory
  rm -rf dist
  mkdir -p dist
  
  # Copy built files
  cp -r apps/web/.next dist/web
  cp -r apps/api/dist dist/api
  cp -r packages/cli/dist dist/cli
  
  # Copy package files
  cp package.json dist/
  cp -r packages dist/
  
  echo "📦 Production bundle created in dist/"
fi