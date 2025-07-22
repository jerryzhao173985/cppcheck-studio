// Enhanced trigger mechanism with better automation
class SimpleTrigger {
    constructor() {
        this.workflowUrl = 'https://github.com/jerryzhao173985/cppcheck-studio/actions/workflows/analyze-on-demand.yml';
        this.apiBase = 'https://jerryzhao173985.github.io/cppcheck-studio/api';
        this.repoApiBase = 'https://api.github.com/repos/jerryzhao173985/cppcheck-studio';
    }
    
    async triggerAnalysis(repository) {
        const analysisId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const triggerTime = new Date().toISOString();
        
        // Store locally with enhanced metadata
        const analyses = JSON.parse(localStorage.getItem('cppcheck-analyses') || '[]');
        analyses.unshift({
            id: analysisId,
            repository,
            status: 'pending',
            timestamp: triggerTime,
            workflowTriggered: false
        });
        localStorage.setItem('cppcheck-analyses', JSON.stringify(analyses.slice(0, 100)));
        
        // Create pre-filled workflow URL
        const params = new URLSearchParams({
            repository: repository,
            analysis_id: analysisId
        });
        const dispatchUrl = `${this.workflowUrl}?${params}`;
        
        // Enhanced instructions with the analysis ID
        return {
            success: true,
            analysisId,
            dispatchUrl,
            repository,
            triggerTime,
            instructions: [
                'Click the button below to open GitHub Actions',
                'Click the "Run workflow" dropdown button',
                'The repository field should show: <strong>' + repository + '</strong>',
                'Optionally add this Analysis ID: <code>' + analysisId + '</code>',
                'Click the green "Run workflow" button to start'
            ],
            tracking: {
                analysisId,
                checkStatusUrl: `${this.apiBase}/status/${analysisId}.json`,
                resultsUrl: `https://jerryzhao173985.github.io/cppcheck-studio/results/${analysisId}/`
            }
        };
    }
    
    async checkAnalysisStatus(analysisId) {
        try {
            // First check status endpoint
            const statusResponse = await fetch(`${this.apiBase}/status/${analysisId}.json?t=${Date.now()}`);
            if (statusResponse.ok) {
                const status = await statusResponse.json();
                return {
                    found: true,
                    status: status.status,
                    data: status
                };
            }
            
            // Then check gallery for completed analyses
            const galleryResponse = await fetch(`${this.apiBase}/gallery.json?t=${Date.now()}`);
            if (galleryResponse.ok) {
                const gallery = await galleryResponse.json();
                const analysis = gallery.analyses?.find(a => a.analysis_id === analysisId);
                if (analysis) {
                    return {
                        found: true,
                        status: 'completed',
                        data: analysis
                    };
                }
            }
        } catch (e) {
            console.log('Status check error:', e);
        }
        
        return {
            found: false,
            status: 'unknown'
        };
    }
    
    async getWorkflowRuns() {
        // This would require authentication, so we'll skip for now
        // In production, this would check actual GitHub workflow runs
        return [];
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