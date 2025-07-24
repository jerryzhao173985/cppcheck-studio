#!/bin/bash
# Monitor cppcheck progress by watching stderr output and updating status
# This runs in the background while cppcheck is executing

set -euo pipefail

# Required environment variables
ANALYSIS_ID="${ANALYSIS_ID:-unknown}"
REPO="${REPO:-unknown}"
WORKFLOW_RUN_ID="${WORKFLOW_RUN_ID:-}"
WORKFLOW_RUN_URL="${WORKFLOW_RUN_URL:-}"
FILE_COUNT="${FILE_COUNT:-0}"
GITHUB_WORKSPACE="${GITHUB_WORKSPACE:-.}"

# Monitor configuration
UPDATE_INTERVAL=10  # Update status every 10 seconds
LOG_FILE="${1:-cppcheck.log}"  # File to monitor for progress
PID_FILE="${2:-monitor.pid}"   # PID file for cleanup
STATUS_DIR="${GITHUB_WORKSPACE}/status_updates"

# Save our PID for cleanup
echo $$ > "$PID_FILE"

# Ensure status directory exists
mkdir -p "$STATUS_DIR"

# Function to update status
update_progress_status() {
    local current_file="$1"
    local message="$2"
    local percentage="$3"
    
    # Calculate fractional step (2.0 to 3.0 represents the analyzing phase)
    # Use awk instead of bc for better portability
    local fractional_step=$(awk "BEGIN {printf \"%.2f\", 2 + ($percentage / 100)}")
    
    # Estimate time remaining based on current progress
    local elapsed=$(($(date +%s) - START_TIME))
    local eta=""
    if [ "$percentage" -gt 0 ] && [ "$percentage" -lt 100 ]; then
        local total_time=$((elapsed * 100 / percentage))
        local remaining=$((total_time - elapsed))
        if [ "$remaining" -gt 0 ]; then
            if [ "$remaining" -lt 60 ]; then
                eta="${remaining}s"
            else
                eta="$((remaining / 60))m $((remaining % 60))s"
            fi
        fi
    fi
    
    # Create status JSON
    cat > "$STATUS_DIR/current_status.json" <<EOF
{
    "analysis_id": "${ANALYSIS_ID}",
    "repository": "${REPO}",
    "status": "running",
    "step": "analyzing",
    "workflow_run_id": "${WORKFLOW_RUN_ID}",
    "workflow_run_url": "${WORKFLOW_RUN_URL}",
    "updated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "message": "${message}",
    "progress": {
        "steps_completed": ${fractional_step},
        "total_steps": 5,
        "current_step": "analyzing",
        "files_found": ${FILE_COUNT},
        "current_file": ${current_file},
        "percentage": ${percentage},
        "elapsed_seconds": ${elapsed},
        "estimated_remaining": "${eta}"
    }
}
EOF
    
    echo "📊 Progress: ${current_file}/${FILE_COUNT} files (${percentage}%) - ETA: ${eta:-calculating...}"
}

# Track start time
START_TIME=$(date +%s)

# Initialize counters
files_processed=0
last_update=0

echo "🔍 Starting progress monitor for ${FILE_COUNT} files..."

# Main monitoring loop
XML_FILE="${LOG_FILE%%.log}-results.xml"  # Convert cppcheck.log to cppcheck-results.xml path
last_xml_size=0
estimated_files=0

while true; do
    # Monitor XML file growth as a proxy for progress
    if [ -f "$XML_FILE" ]; then
        current_xml_size=$(stat -c%s "$XML_FILE" 2>/dev/null || stat -f%z "$XML_FILE" 2>/dev/null || echo "0")
        
        # If XML file is growing, we're making progress
        if [ "$current_xml_size" -gt "$last_xml_size" ]; then
            last_xml_size="$current_xml_size"
            
            # Count error entries in XML as a rough estimate of progress
            # Each file typically generates some output even if no errors
            estimated_files=$(grep -c "<error " "$XML_FILE" 2>/dev/null || echo "0")
            
            # Also check if we have actual progress logs
            if [ -f "$LOG_FILE" ] && [ -s "$LOG_FILE" ]; then
                # If we have log entries, use them
                files_processed=$(grep -c "Checking " "$LOG_FILE" 2>/dev/null || echo "0")
                if [ "$files_processed" -gt 0 ]; then
                    estimated_files="$files_processed"
                fi
            fi
            
            # Calculate percentage based on estimated progress
            percentage=0
            if [ "$FILE_COUNT" -gt 0 ] && [ "$estimated_files" -gt 0 ]; then
                # Use a conservative estimate - assume we're 50% done per file on average
                percentage=$((estimated_files * 50 / FILE_COUNT))
                # Cap at 95% to avoid showing completion before it's done
                if [ "$percentage" -gt 95 ]; then
                    percentage=95
                fi
            fi
            
            # Create progress message
            if [ "$percentage" -eq 0 ]; then
                message="Initializing analysis of ${FILE_COUNT} files..."
            else
                message="Analyzing files... (approximately ${percentage}% complete)"
            fi
            
            # Update status
            update_progress_status "$estimated_files" "$message" "$percentage"
            last_update=$(date +%s)
        fi
    fi
    
    # Also update periodically even if no change detected
    current_time=$(date +%s)
    if [ $((current_time - last_update)) -ge "$UPDATE_INTERVAL" ]; then
        # Use XML file size as a progress indicator
        if [ -f "$XML_FILE" ]; then
            current_size=$(stat -c%s "$XML_FILE" 2>/dev/null || stat -f%z "$XML_FILE" 2>/dev/null || echo "0")
            if [ "$current_size" -gt 0 ]; then
                message="Analysis in progress... (XML size: $((current_size / 1024))KB)"
            else
                message="Waiting for analysis to start..."
            fi
        else
            message="Initializing analysis..."
        fi
        
        # Keep the last known percentage
        update_progress_status "$estimated_files" "$message" "$percentage"
        last_update=$current_time
    fi
    
    # Check if cppcheck process is still running
    # We do this by checking if our parent script is still running
    if [ -f "${LOG_FILE}.done" ]; then
        echo "✅ Analysis complete, stopping monitor"
        break
    fi
    
    # Sleep briefly to avoid excessive CPU usage
    sleep 2
done

# Cleanup
rm -f "$PID_FILE"