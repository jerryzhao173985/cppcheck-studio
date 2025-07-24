#!/bin/bash
# This script creates the status update function
# It's called from the workflow to avoid heredoc issues

cat > status_updates/update_status.sh << 'EOF'
#!/bin/bash
update_analysis_status() {
    local status=$1
    local message=$2
    local step=$3
    
    # Use absolute path to ensure we write to the correct location
    STATUS_DIR="$GITHUB_WORKSPACE/status_updates"
    mkdir -p "$STATUS_DIR"
    
    # Create status JSON
    echo "{
  \"analysis_id\": \"${ANALYSIS_ID}\",
  \"repository\": \"${REPO}\",
  \"status\": \"${status}\",
  \"step\": \"${step}\",
  \"workflow_run_id\": \"${WORKFLOW_RUN_ID}\",
  \"workflow_run_url\": \"${WORKFLOW_RUN_URL}\",
  \"updated_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
  \"message\": \"${message}\",
  \"progress\": {
    \"steps_completed\": ${STEPS_COMPLETED:-0},
    \"total_steps\": 5,
    \"current_step\": \"${step}\",
    \"files_found\": ${FILE_COUNT:-0},
    \"issues_found\": ${ISSUE_COUNT:-0}
  }
}" > "$STATUS_DIR/current_status.json"
    
    echo "📊 Status Update: ${status} - ${message}"
}
EOF

chmod +x status_updates/update_status.sh