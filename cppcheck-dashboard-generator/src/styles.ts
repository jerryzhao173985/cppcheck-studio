/**
 * CSS styles for the virtual scroll dashboard
 */

export function generateStyles(): string {
  return `
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #f5f7fa;
        color: #2d3748;
        line-height: 1.6;
        overflow: hidden;
    }
    
    .container {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        flex-shrink: 0;
    }
    
    .header-content {
        max-width: 1600px;
        margin: 0 auto;
        padding: 0 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }
    
    .header h1 {
        font-size: 1.8em;
        font-weight: 700;
    }
    
    .header-info {
        display: flex;
        gap: 20px;
        font-size: 0.9em;
        opacity: 0.9;
    }
    
    /* Statistics Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        padding: 20px;
        max-width: 1600px;
        margin: 0 auto;
        width: 100%;
        flex-shrink: 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: currentColor;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .stat-card i {
        font-size: 2em;
        margin-bottom: 8px;
        opacity: 0.8;
    }
    
    .stat-card h3 {
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #718096;
        margin-bottom: 8px;
    }
    
    .stat-card .value {
        font-size: 2em;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .stat-card .percent {
        font-size: 0.85em;
        color: #718096;
    }
    
    /* Card colors */
    .stat-card.error { color: #e53e3e; }
    .stat-card.warning { color: #dd6b20; }
    .stat-card.style { color: #5a67d8; }
    .stat-card.performance { color: #38a169; }
    
    /* Controls */
    .controls {
        background: white;
        border-radius: 8px;
        padding: 15px;
        margin: 0 20px;
        max-width: 1560px;
        align-self: center;
        width: calc(100% - 40px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        align-items: center;
        flex-shrink: 0;
    }
    
    .search-container {
        flex: 1;
        min-width: 300px;
        position: relative;
    }
    
    .search-container i {
        position: absolute;
        left: 15px;
        top: 50%;
        transform: translateY(-50%);
        color: #a0aec0;
    }
    
    .search-container input {
        width: 100%;
        padding: 10px 15px 10px 40px;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        font-size: 0.95em;
        transition: border-color 0.2s;
    }
    
    .search-container input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .filter-buttons {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    
    .filter-btn {
        padding: 8px 14px;
        border: 1px solid #e2e8f0;
        background: white;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.85em;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 5px;
        font-family: inherit;
    }
    
    .filter-btn:hover {
        background: #f7fafc;
        transform: translateY(-1px);
    }
    
    .filter-btn.active {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    /* Status bar */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        max-width: 1600px;
        margin: 0 auto;
        width: 100%;
        flex-shrink: 0;
    }
    
    .issues-count {
        font-size: 0.85em;
        color: #718096;
    }
    
    .loading-status {
        font-size: 0.85em;
        color: #667eea;
    }
    
    /* Virtual scroll container */
    .virtual-scroll-container {
        flex: 1;
        overflow-y: auto;
        background: white;
        margin: 0 20px 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        max-width: 1560px;
        align-self: center;
        width: calc(100% - 40px);
    }
    
    .issues-table-wrapper {
        position: relative;
    }
    
    /* Issues Table */
    .issues-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }
    
    .issues-table thead {
        background: #f7fafc;
        border-bottom: 2px solid #e2e8f0;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    
    .issues-table th {
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
        font-size: 0.85em;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #4a5568;
        white-space: nowrap;
    }
    
    /* Column widths - Fixed to prevent shifting */
    .col-indicator { width: 20px; padding: 0 5px; }
    .col-file { width: 25%; }
    .col-line { width: 80px; text-align: center; }
    .col-severity { width: 120px; }
    .col-message { width: calc(100% - 25% - 80px - 120px - 100px - 80px - 20px); }
    .col-id { width: 100px; }
    .col-actions { width: 80px; text-align: center; }
    
    /* Virtual scroll viewport */
    .virtual-scroll-viewport {
        position: relative;
    }
    
    .virtual-scroll-spacer {
        width: 100%;
    }
    
    /* Issue rows */
    .issue-row {
        height: 50px;
        border-bottom: 1px solid #e2e8f0;
        transition: background 0.1s;
        cursor: pointer;
    }
    
    .issue-row:hover {
        background: #f7fafc;
    }
    
    .issue-row td {
        padding: 0 15px;
        font-size: 0.95em;
        height: 50px;
        vertical-align: middle;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    /* Code indicator - Now in separate column */
    .indicator-cell {
        width: 20px;
        padding: 0 5px !important;
    }
    
    .code-indicator {
        width: 4px;
        height: 30px;
        background: #667eea;
        border-radius: 2px;
    }
    
    .file-cell {
        font-family: 'Monaco', 'Consolas', monospace;
        font-size: 0.9em;
        color: #4a5568;
    }
    
    .line-cell {
        font-family: 'Monaco', 'Consolas', monospace;
        color: #718096;
        text-align: center;
    }
    
    .message-cell {
        color: #2d3748;
    }
    
    .id-cell {
        font-family: 'Monaco', 'Consolas', monospace;
        font-size: 0.85em;
        color: #718096;
    }
    
    .actions-cell {
        text-align: center;
    }
    
    .severity-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.75em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .severity-badge.error {
        background: #fed7d7;
        color: #c53030;
    }
    
    .severity-badge.warning {
        background: #feebc8;
        color: #c05621;
    }
    
    .severity-badge.style {
        background: #e0e7ff;
        color: #3730a3;
    }
    
    .severity-badge.performance {
        background: #d1fae5;
        color: #065f46;
    }
    
    .severity-badge.information {
        background: #e0f2fe;
        color: #0369a1;
    }
    
    .severity-badge.unknown {
        background: #e2e8f0;
        color: #4a5568;
    }
    
    .action-btn {
        padding: 6px 10px;
        border: 1px solid #e2e8f0;
        background: white;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9em;
        transition: all 0.2s;
        color: #4a5568;
    }
    
    .action-btn:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
        transform: scale(1.05);
    }
    
    .action-btn.has-code {
        border-color: #667eea;
        color: #667eea;
    }
    
    /* Modal */
    .modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 1000;
        backdrop-filter: blur(4px);
    }
    
    .modal-content {
        background: white;
        margin: 50px auto;
        width: 90%;
        max-width: 1000px;
        max-height: 90vh;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    .modal-header {
        background: #f7fafc;
        padding: 20px;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .modal-header h3 {
        font-size: 1.2em;
        font-weight: 600;
        color: #2d3748;
    }
    
    .close-btn {
        background: none;
        border: none;
        font-size: 1.5em;
        cursor: pointer;
        color: #718096;
        padding: 0;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
        transition: all 0.2s;
    }
    
    .close-btn:hover {
        background: #e2e8f0;
        color: #2d3748;
    }
    
    .modal-body {
        padding: 0;
        max-height: calc(90vh - 80px);
        overflow-y: auto;
    }
    
    /* Issue Details */
    .issue-details {
        padding: 20px;
    }
    
    .info-section, .message-section, .code-section {
        margin-bottom: 25px;
    }
    
    .issue-details h4 {
        font-size: 1em;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .info-table {
        width: 100%;
        background: #f7fafc;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .info-table td {
        padding: 10px 15px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .info-table tr:last-child td {
        border-bottom: none;
    }
    
    .info-table strong {
        color: #4a5568;
        font-weight: 500;
        display: inline-block;
        min-width: 100px;
    }
    
    .code-text {
        font-family: 'Monaco', 'Consolas', monospace;
        font-size: 0.9em;
    }
    
    .message-box {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 15px;
        font-size: 0.95em;
        line-height: 1.6;
    }
    
    /* Code Preview */
    .code-preview {
        background: #1e1e1e;
        border-radius: 8px;
        overflow: hidden;
        position: relative;
    }
    
    .code-preview pre {
        margin: 0;
        padding: 20px;
        overflow-x: auto;
        background: #1e1e1e;
    }
    
    .code-preview code {
        font-family: 'Monaco', 'Consolas', monospace;
        font-size: 0.9em;
        line-height: 1.6;
        color: #d4d4d4;
        display: block;
    }
    
    .highlight-line {
        background: rgba(255, 235, 59, 0.1);
        border-left: 3px solid #ffd600;
        display: block;
        margin: 0 -20px;
        padding: 0 20px;
        padding-left: 17px;
    }
    
    .no-code-message {
        text-align: center;
        padding: 40px;
        color: #718096;
        background: #f7fafc;
        border-radius: 8px;
    }
    
    .no-code-message i {
        font-size: 3em;
        margin-bottom: 15px;
        opacity: 0.5;
    }
    
    .no-code-message p {
        margin: 5px 0;
    }
    
    /* Scrollbar styling */
    .virtual-scroll-container::-webkit-scrollbar {
        width: 10px;
    }
    
    .virtual-scroll-container::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    .virtual-scroll-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 5px;
    }
    
    .virtual-scroll-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-content {
            flex-direction: column;
            text-align: center;
        }
        
        .header-info {
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .stats-grid {
            grid-template-columns: 1fr 1fr;
        }
        
        .filter-buttons {
            justify-content: center;
        }
        
        .col-file { width: 30%; }
        .col-message { width: calc(100% - 30% - 60px - 100px - 80px - 60px - 20px); }
    }
  `;
}
