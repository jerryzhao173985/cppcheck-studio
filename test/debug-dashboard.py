#!/usr/bin/env python3
"""
Generate a debug version of the dashboard to find the issue
"""

import json
import sys
import os

def generate_debug_dashboard(json_file, output_file):
    # Read the analysis data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    issues = data.get('issues', [])
    print(f"Total issues in JSON: {len(issues)}")
    
    # Simple test data
    test_issues = [
        {
            "file": "test/file1.cpp",
            "location": {"line": 10},
            "line": 10,
            "severity": "error",
            "message": "Test error message",
            "id": "testError1",
            "code_context": {
                "lines": [
                    {"number": 8, "content": "void test() {"},
                    {"number": 9, "content": "    int x = 5;"},
                    {"number": 10, "content": "    return x;", "is_target": True},
                    {"number": 11, "content": "}"}
                ],
                "target_line": 10
            }
        },
        {
            "file": "test/file2.cpp",
            "location": {"line": 20},
            "line": 20,
            "severity": "warning",
            "message": "Test warning message",
            "id": "testWarning1"
        }
    ]
    
    # Generate the dashboard HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Debug CPPCheck Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
        .debug {{ background-color: #f0f0f0; padding: 10px; margin: 10px 0; }}
        button {{ padding: 5px 10px; margin: 2px; cursor: pointer; }}
    </style>
</head>
<body>
    <h1>Debug CPPCheck Dashboard</h1>
    
    <div class="debug">
        <h3>Debug Information</h3>
        <p>Total issues from JSON: {len(issues)}</p>
        <p>Test issues: {len(test_issues)}</p>
        <p id="jsDebug"></p>
    </div>
    
    <h2>Issues Table</h2>
    <table>
        <thead>
            <tr>
                <th>File</th>
                <th>Line</th>
                <th>Severity</th>
                <th>Message</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody id="issuesBody">
            <!-- Will be populated by JavaScript -->
        </tbody>
    </table>
    
    <div id="modal" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); background:white; border:2px solid black; padding:20px; max-width:80%; max-height:80%; overflow:auto;">
        <h3 id="modalTitle"></h3>
        <div id="modalContent"></div>
        <button onclick="closeModal()">Close</button>
    </div>
    
    <script>
        // Test issues data
        const testIssues = {json.dumps(test_issues)};
        
        // Debug info
        const debugEl = document.getElementById('jsDebug');
        debugEl.innerHTML = `JavaScript loaded. Test issues: ${{testIssues.length}}`;
        
        // Function to show issue details
        function showIssue(index) {{
            const issue = testIssues[index];
            const modal = document.getElementById('modal');
            const title = document.getElementById('modalTitle');
            const content = document.getElementById('modalContent');
            
            title.textContent = `${{issue.file}}:${{issue.line}}`;
            
            let html = `<p><strong>Severity:</strong> ${{issue.severity}}</p>`;
            html += `<p><strong>Message:</strong> ${{issue.message}}</p>`;
            
            if (issue.code_context) {{
                html += '<h4>Code Context:</h4><pre>';
                issue.code_context.lines.forEach(line => {{
                    const style = line.is_target ? 'background-color: yellow;' : '';
                    html += `<div style="${{style}}">${{line.number}}: ${{escapeHtml(line.content)}}</div>`;
                }});
                html += '</pre>';
            }} else {{
                html += '<p>No code context available</p>';
            }}
            
            content.innerHTML = html;
            modal.style.display = 'block';
        }}
        
        function closeModal() {{
            document.getElementById('modal').style.display = 'none';
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        // Render the table
        function renderTable() {{
            const tbody = document.getElementById('issuesBody');
            tbody.innerHTML = '';
            
            testIssues.forEach((issue, index) => {{
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${{issue.file}}</td>
                    <td>${{issue.line}}</td>
                    <td class="${{issue.severity}}">${{issue.severity}}</td>
                    <td>${{issue.message}}</td>
                    <td><button onclick="showIssue(${{index}})">View</button></td>
                `;
                tbody.appendChild(row);
            }});
            
            debugEl.innerHTML += `<br>Table rendered with ${{tbody.children.length}} rows`;
        }}
        
        // Render on load
        renderTable();
    </script>
</body>
</html>'''
    
    # Write the dashboard
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Debug dashboard generated: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python debug-dashboard.py <analysis.json> <output.html>")
        sys.exit(1)
    
    generate_debug_dashboard(sys.argv[1], sys.argv[2])