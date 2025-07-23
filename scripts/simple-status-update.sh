#!/bin/bash
# Simple status update function that avoids heredoc complexity

update_analysis_status() {
    local status=$1
    local message=$2
    local step=$3
    
    # Create status directory
    STATUS_DIR="$GITHUB_WORKSPACE/status_updates"
    mkdir -p "$STATUS_DIR"
    
    # Create status JSON using jq for proper escaping
    jq -n \
        --arg aid "${ANALYSIS_ID}" \
        --arg repo "${REPO}" \
        --arg status "${status}" \
        --arg step "${step}" \
        --arg wfid "${WORKFLOW_RUN_ID}" \
        --arg wfurl "${WORKFLOW_RUN_URL}" \
        --arg msg "${message}" \
        --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --argjson sc "${STEPS_COMPLETED:-0}" \
        --argjson fc "${FILE_COUNT:-0}" \
        --argjson ic "${ISSUE_COUNT:-0}" \
        '{
            analysis_id: $aid,
            repository: $repo,
            status: $status,
            step: $step,
            workflow_run_id: $wfid,
            workflow_run_url: $wfurl,
            updated_at: $ts,
            message: $msg,
            progress: {
                steps_completed: $sc,
                total_steps: 5,
                current_step: $step,
                files_found: $fc,
                issues_found: $ic
            }
        }' > "$STATUS_DIR/current_status.json"
    
    echo "📊 Status Update: ${status} - ${message}"
}