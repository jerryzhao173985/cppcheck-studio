#!/bin/bash

# Script to manually process analysis artifacts

RUN_ID=$1
if [ -z "$RUN_ID" ]; then
    echo "Usage: $0 <run-id>"
    echo "Example: $0 16443335387"
    exit 1
fi

# Download artifacts
echo "Downloading artifacts from run $RUN_ID..."
gh run download $RUN_ID -D temp-artifacts

# Find metadata
METADATA_FILE=$(find temp-artifacts -name "metadata.json" | head -1)
if [ -z "$METADATA_FILE" ]; then
    echo "No metadata.json found in artifacts"
    exit 1
fi

# Parse metadata
ANALYSIS_ID=$(jq -r .analysis_id "$METADATA_FILE")
REPO=$(jq -r .repository "$METADATA_FILE")
DASHBOARD=$(find temp-artifacts -name "dashboard-*.html" | head -1)

echo "Found analysis for $REPO (ID: $ANALYSIS_ID)"

# Create results directory
mkdir -p docs/results/$ANALYSIS_ID
mkdir -p docs/api/repos

# Copy files
cp "$DASHBOARD" "docs/results/$ANALYSIS_ID/index.html"
cp "$METADATA_FILE" "docs/results/$ANALYSIS_ID/"

# Update gallery
GALLERY_FILE="docs/api/gallery.json"
if [ -f "$GALLERY_FILE" ]; then
    # Add to existing gallery
    jq --slurpfile new "$METADATA_FILE" '.analyses = ([$new[0]] + .analyses | unique_by(.repository))' "$GALLERY_FILE" > temp.json
    mv temp.json "$GALLERY_FILE"
else
    # Create new gallery
    jq -n --slurpfile metadata "$METADATA_FILE" '{analyses: [$metadata[0]]}' > "$GALLERY_FILE"
fi

# Copy to main API
cp "$GALLERY_FILE" docs/api/index.json

# Create repo-specific file
REPO_SAFE=$(echo "$REPO" | tr '/' '_')
cp "$METADATA_FILE" "docs/api/repos/${REPO_SAFE}.json"

# Clean up
rm -rf temp-artifacts

echo "✅ Analysis results processed successfully!"
echo "Dashboard available at: docs/results/$ANALYSIS_ID/index.html"
echo "Gallery updated at: docs/api/gallery.json"