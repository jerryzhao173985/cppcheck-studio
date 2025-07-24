import { Router } from 'express'
import { z } from 'zod'
import { MetricsCollector } from '@cppcheck-studio/core'
import { asyncHandler } from '../middleware/async'
import { validateRequest } from '../middleware/validate'

export const metricsRouter = Router()

const getMetricsSchema = z.object({
  query: z.object({
    projectId: z.string().optional(),
    startDate: z.string().optional(),
    endDate: z.string().optional(),
    groupBy: z.enum(['day', 'week', 'month']).optional()
  })
})

// Get metrics
metricsRouter.get(
  '/',
  validateRequest(getMetricsSchema),
  asyncHandler(async (req, res) => {
    const { projectId, startDate, endDate, groupBy = 'day' } = req.query

    const collector = new MetricsCollector()
    const metrics = await collector.getMetrics({
      projectId,
      startDate: startDate ? new Date(startDate) : undefined,
      endDate: endDate ? new Date(endDate) : undefined,
      groupBy
    })

    res.json(metrics)
  })
)

// Get summary metrics
metricsRouter.get(
  '/summary',
  asyncHandler(async (req, res) => {
    const { projectId } = req.query

    const collector = new MetricsCollector()
    const summary = await collector.getSummary({ projectId })

    res.json(summary)
  })
)

// Get trends
metricsRouter.get(
  '/trends',
  asyncHandler(async (req, res) => {
    const { projectId, days = 30 } = req.query

    const collector = new MetricsCollector()
    const trends = await collector.getTrends({
      projectId,
      days: Number(days)
    })

    res.json(trends)
  })
)

// Export metrics
metricsRouter.get(
  '/export',
  asyncHandler(async (req, res) => {
    const { format = 'csv', projectId } = req.query

    const collector = new MetricsCollector()
    const data = await collector.export({
      format: format as 'csv' | 'json',
      projectId
    })

    if (format === 'csv') {
      res.setHeader('Content-Type', 'text/csv')
      res.setHeader('Content-Disposition', 'attachment; filename=metrics.csv')
    }

    res.send(data)
  })
)