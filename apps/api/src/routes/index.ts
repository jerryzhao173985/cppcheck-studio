import { Router } from 'express'
import { analysisRouter } from './analysis'
import { projectRouter } from './projects'
import { fixRouter } from './fixes'
import { metricsRouter } from './metrics'
import { rulesRouter } from './rules'

export const router = Router()

router.use('/analysis', analysisRouter)
router.use('/projects', projectRouter)
router.use('/fixes', fixRouter)
router.use('/metrics', metricsRouter)
router.use('/rules', rulesRouter)

// API info
router.get('/', (req, res) => {
  res.json({
    name: 'CPPCheck Studio API',
    version: '1.0.0',
    endpoints: {
      analysis: '/api/analysis',
      projects: '/api/projects',
      fixes: '/api/fixes',
      metrics: '/api/metrics',
      rules: '/api/rules'
    }
  })
})