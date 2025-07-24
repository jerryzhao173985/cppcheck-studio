import { Router } from 'express'
import { z } from 'zod'
import { CppcheckAnalyzer } from '@cppcheck-studio/core'
import { logger } from '../lib/logger'
import { asyncHandler } from '../middleware/async'
import { validateRequest } from '../middleware/validate'

export const analysisRouter = Router()

const analyzeSchema = z.object({
  body: z.object({
    projectPath: z.string(),
    profile: z.enum(['quick', 'full', 'cpp17', 'cpp20', 'memory', 'performance']).optional(),
    incremental: z.boolean().optional(),
    paths: z.array(z.string()).optional(),
    exclude: z.array(z.string()).optional()
  })
})

const getAnalysisSchema = z.object({
  params: z.object({
    id: z.string().uuid()
  })
})

// Start a new analysis
analysisRouter.post(
  '/',
  validateRequest(analyzeSchema),
  asyncHandler(async (req, res) => {
    const { projectPath, profile = 'quick', incremental = true, paths, exclude } = req.body

    const analyzer = new CppcheckAnalyzer({
      projectPath,
      profile,
      incremental,
      paths,
      exclude
    })

    // Start analysis in background
    const analysisId = analyzer.startAsync()

    res.status(202).json({
      id: analysisId,
      status: 'started',
      message: 'Analysis started in background'
    })
  })
)

// Get analysis status
analysisRouter.get(
  '/:id',
  validateRequest(getAnalysisSchema),
  asyncHandler(async (req, res) => {
    const { id } = req.params

    // Get analysis status from analyzer
    const status = await CppcheckAnalyzer.getStatus(id)

    if (!status) {
      return res.status(404).json({ error: 'Analysis not found' })
    }

    res.json(status)
  })
)

// Get all analyses
analysisRouter.get(
  '/',
  asyncHandler(async (req, res) => {
    const analyses = await CppcheckAnalyzer.listAnalyses()
    res.json(analyses)
  })
)

// Cancel analysis
analysisRouter.delete(
  '/:id',
  validateRequest(getAnalysisSchema),
  asyncHandler(async (req, res) => {
    const { id } = req.params

    const success = await CppcheckAnalyzer.cancel(id)

    if (!success) {
      return res.status(404).json({ error: 'Analysis not found' })
    }

    res.json({ message: 'Analysis cancelled' })
  })
)