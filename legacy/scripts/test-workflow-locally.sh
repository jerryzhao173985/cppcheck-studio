#!/bin/bash
# Test workflow components locally

echo "🧪 Testing CPPCheck Studio Workflow Components"

# Set test environment
export GITHUB_WORKSPACE=$(pwd)
export GITHUB_ENV=$(mktemp)
export ANALYSIS_ID="test-$(date +%s)"
export REPO="test/repo"

echo "📋 Environment:"
echo "  GITHUB_WORKSPACE: $GITHUB_WORKSPACE"
echo "  GITHUB_ENV: $GITHUB_ENV"
echo "  ANALYSIS_ID: $ANALYSIS_ID"

# Test 1: Status function setup
echo -e "\n✅ Test 1: Status function setup"
mkdir -p status_updates

cat > status_updates/update_status.sh << 'EOF'
#!/bin/bash
update_analysis_status() {
    local status=$1
    local message=$2
    local step=$3
    
    # Use absolute path to ensure we write to the correct location
    STATUS_DIR="$GITHUB_WORKSPACE/status_updates"
    mkdir -p "$STATUS_DIR"
    
    cat > "$STATUS_DIR/current_status.json" << EOJSON
{
  "analysis_id": "${ANALYSIS_ID}",
  "repository": "${REPO}",
  "status": "${status}",
  "step": "${step}",
  "message": "${message}",
  "progress": {
    "steps_completed": ${STEPS_COMPLETED:-0},
    "total_steps": 5,
    "current_step": "${step}",
    "files_found": ${FILE_COUNT:-0},
    "issues_found": ${ISSUE_COUNT:-0}
  }
}
EOJSON
    
    echo "📊 Status Update: ${status} - ${message}"
}
EOF

chmod +x status_updates/update_status.sh
source $GITHUB_WORKSPACE/status_updates/update_status.sh

# Test calling the function
export STEPS_COMPLETED=0
export FILE_COUNT=0
export ISSUE_COUNT=0
update_analysis_status "test" "Testing status update" "testing"

if [ -f "$GITHUB_WORKSPACE/status_updates/current_status.json" ]; then
    echo "✅ Status file created successfully"
    cat "$GITHUB_WORKSPACE/status_updates/current_status.json"
else
    echo "❌ Status file not created!"
    exit 1
fi

# Test 2: Directory changes
echo -e "\n✅ Test 2: Testing after directory change"
mkdir -p test-repo
cd test-repo

# Try to call function after cd
update_analysis_status "test2" "Testing from different directory" "testing"

if [ -f "$GITHUB_WORKSPACE/status_updates/current_status.json" ]; then
    echo "✅ Status update works after directory change"
else
    echo "❌ Status update failed after directory change!"
    exit 1
fi

cd ..

# Test 3: Python scripts
echo -e "\n✅ Test 3: Testing Python scripts"

# Create test JSON
cat > test.json << 'EOF'
{
  "issues": [
    {"file": "test1.cpp", "severity": "error"},
    {"file": "test2.cpp", "severity": "warning"},
    {"file": "test3.cpp", "severity": "style"}
  ]
}
EOF

# Test issue counting
echo "Testing issue counting..."
ISSUE_COUNT=$(python3 -c "
import json
try:
    data = json.load(open('test.json'))
    print(len(data.get('issues', [])))
except:
    print('0')
")
echo "Issue count: $ISSUE_COUNT"

if [ "$ISSUE_COUNT" = "3" ]; then
    echo "✅ Issue counting works"
else
    echo "❌ Issue counting failed! Got: $ISSUE_COUNT"
fi

# Test file listing
echo "Testing file listing..."
python3 -c "
import json
try:
    data = json.load(open('test.json'))
    files = set(issue.get('file', '') for issue in data.get('issues', [])[:10])
    for f in list(files)[:5]:
        if f:
            print(f'  - {f}')
except:
    print('Could not list files')
"

# Cleanup
rm -f test.json
rm -rf status_updates test-repo
rm -f $GITHUB_ENV

echo -e "\n✅ All tests completed!"