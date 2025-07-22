/**
 * CPPCheck Studio Client Library
 * This can be included in your web pages to trigger analysis
 */

class CPPCheckClient {
    constructor(options = {}) {
        // In production, use your backend service URL
        this.apiUrl = options.apiUrl || 'https://api.cppcheck.studio';
        this.githubToken = options.githubToken; // Only for direct GitHub API calls (not recommended for frontend)
    }
    
    /**
     * Parse repository URL into owner/repo format
     */
    parseRepoUrl(input) {
        input = input.trim();
        
        // Handle different GitHub URL formats
        const patterns = [
            /github\.com[\/:]([^\/]+)\/([^\/\.]+)(?:\.git)?$/,
            /^([^\/]+)\/([^\/]+)$/
        ];
        
        for (const pattern of patterns) {
            const match = input.match(pattern);
            if (match) {
                return `${match[1]}/${match[2]}`;
            }
        }
        
        return null;
    }
    
    /**
     * Trigger analysis via backend service (recommended)
     */
    async analyzeRepository(repoUrl, options = {}) {
        const repository = this.parseRepoUrl(repoUrl);
        if (!repository) {
            throw new Error('Invalid repository URL format');
        }
        
        const response = await fetch(`${this.apiUrl}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                repository,
                branch: options.branch || 'main',
                maxFiles: options.maxFiles || 500
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to trigger analysis');
        }
        
        return response.json();
    }
    
    /**
     * Check analysis status
     */
    async checkStatus(analysisId) {
        const response = await fetch(`${this.apiUrl}/api/analysis/${analysisId}/status`);
        
        if (!response.ok) {
            throw new Error('Failed to check analysis status');
        }
        
        return response.json();
    }
    
    /**
     * Get analysis results
     */
    async getResults(analysisId) {
        const response = await fetch(`${this.apiUrl}/api/analysis/${analysisId}/results`);
        
        if (!response.ok) {
            throw new Error('Failed to get analysis results');
        }
        
        return response.json();
    }
    
    /**
     * Poll for analysis completion
     */
    async waitForCompletion(analysisId, options = {}) {
        const maxAttempts = options.maxAttempts || 60; // 5 minutes with 5s intervals
        const interval = options.interval || 5000; // 5 seconds
        
        for (let i = 0; i < maxAttempts; i++) {
            const status = await this.checkStatus(analysisId);
            
            if (status.status === 'completed') {
                return await this.getResults(analysisId);
            }
            
            if (status.status === 'failed') {
                throw new Error('Analysis failed: ' + (status.error || 'Unknown error'));
            }
            
            // Wait before next check
            await new Promise(resolve => setTimeout(resolve, interval));
        }
        
        throw new Error('Analysis timed out');
    }
    
    /**
     * Direct GitHub API call (only use in secure environments)
     */
    async triggerViaGitHub(repository, options = {}) {
        if (!this.githubToken) {
            throw new Error('GitHub token not configured');
        }
        
        const response = await fetch('https://api.github.com/repos/jerryzhao173985/cppcheck-studio/dispatches', {
            method: 'POST',
            headers: {
                'Accept': 'application/vnd.github+json',
                'Authorization': `Bearer ${this.githubToken}`,
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                event_type: 'analyze-repo',
                client_payload: {
                    repository,
                    branch: options.branch || 'main',
                    max_files: options.maxFiles || 500
                }
            })
        });
        
        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status}`);
        }
        
        return {
            success: true,
            message: 'Analysis triggered via GitHub'
        };
    }
}

// Example usage in a web page:
/*
const client = new CPPCheckClient({
    apiUrl: 'http://localhost:3000' // Your backend service
});

async function analyzeRepo() {
    const repoUrl = document.getElementById('repoInput').value;
    
    try {
        // Show loading state
        showStatus('info', 'Triggering analysis...');
        
        // Trigger analysis
        const result = await client.analyzeRepository(repoUrl, {
            branch: 'main',
            maxFiles: 500
        });
        
        showStatus('info', `Analysis started! ID: ${result.analysisId}`);
        
        // Wait for completion
        const analysis = await client.waitForCompletion(result.analysisId);
        
        // Show results
        showStatus('success', 'Analysis complete!');
        window.location.href = analysis.dashboardUrl;
        
    } catch (error) {
        showStatus('error', error.message);
    }
}
*/

// For demo purposes, simulate the backend
class CPPCheckDemo {
    static async simulateAnalysis(repository, options = {}) {
        // Show loading
        console.log(`🔄 Starting analysis for ${repository}...`);
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const analysisId = Date.now().toString();
        
        console.log(`✅ Analysis triggered! ID: ${analysisId}`);
        
        // Simulate processing
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Return mock results
        return {
            success: true,
            analysisId,
            repository,
            dashboardUrl: 'dashboard.html', // In production: `/results/${analysisId}/dashboard.html`
            summary: {
                filesAnalyzed: Math.floor(Math.random() * 500) + 50,
                totalIssues: Math.floor(Math.random() * 200) + 10,
                errors: Math.floor(Math.random() * 20),
                warnings: Math.floor(Math.random() * 30),
                style: Math.floor(Math.random() * 100),
                performance: Math.floor(Math.random() * 10)
            }
        };
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CPPCheckClient, CPPCheckDemo };
}