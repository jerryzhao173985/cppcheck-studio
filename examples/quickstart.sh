#!/bin/bash
# Quick example: Generate dashboard from cppcheck output

echo "🔍 Running cppcheck on sample code..."
cppcheck --enable=all --xml --xml-version=2 . 2> analysis.xml

echo "🔄 Converting XML to JSON..."
python3 ../utils/xml2json-simple.py analysis.xml > analysis.json

echo "📊 Generating dashboard..."
python3 ../generate/generate-standalone-virtual-dashboard.py analysis.json dashboard.html

echo "✅ Dashboard created: dashboard.html"
echo "   Open in your browser to view results"
