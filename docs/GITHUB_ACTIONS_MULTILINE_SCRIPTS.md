# GitHub Actions Multi-line Scripts Best Practices

This document outlines the proper way to handle multi-line scripts in GitHub Actions YAML files, based on the lessons learned from fixing the analyze-on-demand workflow.

## The Problem

GitHub Actions YAML files can have parsing errors when using heredoc syntax incorrectly. The original error occurred because of improper heredoc delimiter usage:

```yaml
# INCORRECT - This causes YAML parsing errors
cat > status_updates/update_status.sh << 'EOF'
#!/bin/bash
update_analysis_status() {
    # ...
}
EOF
```

## The Solution

Use a unique delimiter for the outer heredoc to avoid conflicts with inner heredocs:

```yaml
# CORRECT - Use a unique delimiter like 'SCRIPT_EOF'
cat > status_updates/update_status.sh << 'SCRIPT_EOF'
#!/bin/bash
update_analysis_status() {
    # ... script content ...
    # Can use EOF internally without conflicts
    cat > file.json << EOF
    {
        "key": "value"
    }
    EOF
}
SCRIPT_EOF
```

## Best Practices

### 1. Use Unique Heredoc Delimiters

When embedding scripts that contain their own heredocs, use unique delimiters:

```yaml
- name: Create script with nested heredocs
  run: |
    cat > my_script.sh << 'OUTER_EOF'
    #!/bin/bash
    
    # This script can now safely use EOF internally
    cat > config.json << EOF
    {
        "setting": "value"
    }
    EOF
    
    OUTER_EOF
```

### 2. Use Inline Python for Simple Scripts

For simple Python scripts, use inline syntax to avoid heredoc issues:

```yaml
- name: Count issues
  run: |
    ISSUE_COUNT=$(python3 -c "
    import json
    try:
        with open('analysis.json', 'r') as f:
            data = json.load(f)
        print(len(data.get('issues', [])))
    except Exception:
        print('0')
    ")
```

### 3. Alternative: Use Base64 Encoding

For complex scripts with special characters, consider base64 encoding:

```yaml
- name: Create complex script
  run: |
    echo 'IyEvYmluL2Jhc2gKZWNobyAiSGVsbG8gV29ybGQi' | base64 -d > script.sh
    chmod +x script.sh
    ./script.sh
```

### 4. Alternative: Store Scripts as Files

For complex scripts, store them in the repository and execute them:

```yaml
- name: Run complex script
  run: |
    chmod +x scripts/complex-script.sh
    ./scripts/complex-script.sh
```

## Common Pitfalls

### 1. Nested EOF Delimiters

**Problem:**
```yaml
cat > script.sh << 'EOF'
cat > file.txt << EOF
content
EOF
EOF  # This EOF is ambiguous!
```

**Solution:**
```yaml
cat > script.sh << 'SCRIPT_EOF'
cat > file.txt << EOF
content
EOF
SCRIPT_EOF
```

### 2. Variable Expansion in Heredocs

**Single-quoted delimiter** (no variable expansion):
```yaml
cat > script.sh << 'EOF'
echo "$VARIABLE"  # Will output literally: $VARIABLE
EOF
```

**Unquoted delimiter** (with variable expansion):
```yaml
cat > script.sh << EOF
echo "$VARIABLE"  # Will expand the variable
EOF
```

### 3. YAML Multi-line Strings

GitHub Actions supports YAML folded style for simple multi-line commands:

```yaml
- name: Run multi-line command
  run: >
    for file in *.txt; do
      echo "Processing $file";
      cat "$file";
    done
```

## Real-World Example

Here's how we fixed the status tracking function in our workflow:

```yaml
- name: Setup status tracking
  run: |
    mkdir -p status_updates
    
    # Create status update script with unique delimiter
    cat > status_updates/update_status.sh << 'SCRIPT_EOF'
    #!/bin/bash
    update_analysis_status() {
        local status=$1
        local message=$2
        local step=$3
        
        STATUS_DIR="$GITHUB_WORKSPACE/status_updates"
        mkdir -p "$STATUS_DIR"
        
        # Now we can safely use EOF for the JSON heredoc
        cat > "$STATUS_DIR/current_status.json" << EOJSON
    {
      "analysis_id": "${ANALYSIS_ID}",
      "repository": "${REPO}",
      "status": "${status}",
      "step": "${step}",
      "message": "${message}"
    }
    EOJSON
        
        echo "📊 Status Update: ${status} - ${message}"
    }
    SCRIPT_EOF
    
    chmod +x status_updates/update_status.sh
    source $GITHUB_WORKSPACE/status_updates/update_status.sh
```

## Testing Your Scripts Locally

Before pushing to GitHub, test your workflow scripts locally:

```bash
#!/bin/bash
# Simulate GitHub Actions environment
export GITHUB_WORKSPACE=$(pwd)
export GITHUB_ENV=$(mktemp)

# Test your script here
# ...

# Cleanup
rm -f $GITHUB_ENV
```

## Summary

1. **Use unique heredoc delimiters** when nesting heredocs (e.g., `SCRIPT_EOF`, `OUTER_EOF`)
2. **Use inline Python/Bash** for simple scripts to avoid heredoc complexity
3. **Consider storing complex scripts as files** in your repository
4. **Test locally** before pushing to avoid workflow failures
5. **Be aware of variable expansion** differences between quoted and unquoted heredoc delimiters

By following these practices, you can avoid YAML parsing errors and create maintainable GitHub Actions workflows with complex multi-line scripts.