// Simple trigger mechanism using GitHub workflow dispatch
class SimpleTrigger {
    constructor() {
        this.workflowUrl = 'https://github.com/jerryzhao173985/cppcheck-studio/actions/workflows/process-analysis-request.yml';
        this.apiBase = 'https://jerryzhao173985.github.io/cppcheck-studio/api';
    }
    
    async triggerAnalysis(repository) {
        const analysisId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        // Store locally
        const analyses = JSON.parse(localStorage.getItem('analyses') || '[]');
        analyses.unshift({
            id: analysisId,
            repository,
            status: 'pending',
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('analyses', JSON.stringify(analyses.slice(0, 100)));
        
        // Return workflow dispatch URL with pre-filled repository
        const dispatchUrl = `${this.workflowUrl}?repository=${encodeURIComponent(repository)}`;
        
        return {
            success: true,
            analysisId,
            dispatchUrl,
            instructions: [
                'Click the button below to trigger analysis',
                'On the GitHub page, click "Run workflow"',
                'The repository field will be pre-filled',
                'Click the green "Run workflow" button'
            ]
        };
    }
    
    async checkAnalyses() {
        try {
            // Try to fetch from GitHub Pages API
            const response = await fetch(`${this.apiBase}/index.json?t=${Date.now()}`);
            if (response.ok) {
                const data = await response.json();
                return data.analyses || [];
            }
        } catch (e) {
            console.log('Using local data:', e);
        }
        
        // Fall back to local storage
        return JSON.parse(localStorage.getItem('analyses') || '[]');
    }
    
    async updateLocalAnalyses() {
        const remoteAnalyses = await this.checkAnalyses();
        const localAnalyses = JSON.parse(localStorage.getItem('analyses') || '[]');
        
        // Merge remote results with local
        const merged = [...remoteAnalyses];
        localAnalyses.forEach(local => {
            if (!merged.find(r => r.repository === local.repository && 
                              Math.abs(new Date(r.timestamp) - new Date(local.timestamp)) < 60000)) {
                merged.push(local);
            }
        });
        
        // Sort by timestamp
        merged.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        // Store merged results
        localStorage.setItem('analyses', JSON.stringify(merged.slice(0, 100)));
        
        return merged;
    }
}

window.SimpleTrigger = SimpleTrigger;