// Example Node.js service for triggering CPPCheck analysis
// This would typically run on a server or as a serverless function

const GITHUB_TOKEN = process.env.GITHUB_TOKEN; // Store securely!
const GITHUB_REPO = 'jerryzhao173985/cppcheck-studio';

/**
 * Trigger CPPCheck analysis for a repository
 * @param {string} repository - Repository in owner/repo format
 * @param {string} branch - Branch to analyze (default: main)
 * @param {number} maxFiles - Maximum files to analyze (default: 500)
 * @returns {Promise<{success: boolean, analysisId?: string, error?: string}>}
 */
async function triggerAnalysis(repository, branch = 'main', maxFiles = 500) {
    if (!GITHUB_TOKEN) {
        return { success: false, error: 'GitHub token not configured' };
    }
    
    // Validate repository format
    const repoMatch = repository.match(/^[a-zA-Z0-9-]+\/[a-zA-Z0-9-_.]+$/);
    if (!repoMatch) {
        return { success: false, error: 'Invalid repository format' };
    }
    
    const analysisId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    try {
        const response = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/dispatches`, {
            method: 'POST',
            headers: {
                'Accept': 'application/vnd.github+json',
                'Authorization': `Bearer ${GITHUB_TOKEN}`,
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                event_type: 'analyze-repo',
                client_payload: {
                    repository,
                    branch,
                    max_files: maxFiles,
                    analysis_id: analysisId,
                    callback_url: process.env.CALLBACK_URL || null
                }
            })
        });
        
        if (!response.ok) {
            const error = await response.text();
            return { success: false, error: `GitHub API error: ${response.status} - ${error}` };
        }
        
        return { 
            success: true, 
            analysisId,
            message: 'Analysis triggered successfully',
            estimatedTime: '2-5 minutes'
        };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Check analysis status (would query your database in production)
 * @param {string} analysisId - The analysis ID to check
 * @returns {Promise<object>} Analysis status
 */
async function checkAnalysisStatus(analysisId) {
    // In production, this would query your database
    // For now, we'll return a mock response
    return {
        analysisId,
        status: 'in_progress',
        startedAt: new Date().toISOString(),
        estimatedCompletion: '2 minutes'
    };
}

/**
 * Get analysis results
 * @param {string} analysisId - The analysis ID
 * @returns {Promise<object>} Analysis results
 */
async function getAnalysisResults(analysisId) {
    // In production, this would fetch from your storage
    return {
        analysisId,
        status: 'completed',
        dashboardUrl: `https://jerryzhao173985.github.io/cppcheck-studio/results/${analysisId}/dashboard.html`,
        summary: {
            filesAnalyzed: 150,
            totalIssues: 42,
            errors: 5,
            warnings: 12,
            style: 20,
            performance: 5
        }
    };
}

// Express.js example endpoint
const express = require('express');
const app = express();
app.use(express.json());

// CORS for web requests
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

// Trigger analysis endpoint
app.post('/api/analyze', async (req, res) => {
    const { repository, branch, maxFiles } = req.body;
    
    if (!repository) {
        return res.status(400).json({ error: 'Repository is required' });
    }
    
    const result = await triggerAnalysis(repository, branch, maxFiles);
    
    if (result.success) {
        res.json(result);
    } else {
        res.status(400).json(result);
    }
});

// Check status endpoint
app.get('/api/analysis/:id/status', async (req, res) => {
    const status = await checkAnalysisStatus(req.params.id);
    res.json(status);
});

// Get results endpoint
app.get('/api/analysis/:id/results', async (req, res) => {
    const results = await getAnalysisResults(req.params.id);
    res.json(results);
});

// Webhook endpoint for GitHub to call when analysis completes
app.post('/api/webhook/analysis-complete', (req, res) => {
    const { analysis_id, repository, issues_found, dashboard_url } = req.body;
    
    // Store results in database
    console.log(`Analysis ${analysis_id} completed for ${repository}`);
    console.log(`Found ${issues_found} issues`);
    console.log(`Dashboard: ${dashboard_url}`);
    
    // You could send email notifications, update UI, etc.
    
    res.json({ received: true });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`CPPCheck trigger service running on port ${PORT}`);
});

// Example usage:
// curl -X POST http://localhost:3000/api/analyze \
//   -H "Content-Type: application/json" \
//   -d '{"repository": "nlohmann/json", "branch": "develop"}'