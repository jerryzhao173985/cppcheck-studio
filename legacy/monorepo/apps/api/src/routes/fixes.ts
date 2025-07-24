import { Router } from 'express'
import { z } from 'zod'
import { FixGenerator } from '@cppcheck-studio/core'
import { asyncHandler } from '../middleware/async'
import { validateRequest } from '../middleware/validate'

export const fixRouter = Router()

const previewFixSchema = z.object({
  body: z.object({
    issue: z.object({
      file: z.string(),
      line: z.number(),
      column: z.number(),
      id: z.string(),
      severity: z.string(),
      message: z.string()
    })
  })
})

const applyFixSchema = z.object({
  body: z.object({
    fixes: z.array(z.object({
      file: z.string(),
      original: z.string(),
      fixed: z.string(),
      issueId: z.string()
    })),
    dryRun: z.boolean().optional()
  })
})

// Preview fix for an issue
fixRouter.post(
  '/preview',
  validateRequest(previewFixSchema),
  asyncHandler(async (req, res) => {
    const { issue } = req.body

    const generator = new FixGenerator()
    const fix = await generator.generateFix(issue)

    if (!fix) {
      return res.status(404).json({ error: 'No fix available for this issue' })
    }

    res.json(fix)
  })
)

// Apply fixes
fixRouter.post(
  '/apply',
  validateRequest(applyFixSchema),
  asyncHandler(async (req, res) => {
    const { fixes, dryRun = false } = req.body

    const generator = new FixGenerator()
    const results = await generator.applyFixes(fixes, { dryRun })

    res.json({
      applied: results.applied,
      failed: results.failed,
      dryRun,
      backupPath: results.backupPath
    })
  })
)

// Get fix history
fixRouter.get(
  '/history',
  asyncHandler(async (req, res) => {
    const generator = new FixGenerator()
    const history = await generator.getHistory()

    res.json(history)
  })
)

// Revert fixes
fixRouter.post(
  '/revert/:id',
  asyncHandler(async (req, res) => {
    const { id } = req.params

    const generator = new FixGenerator()
    const success = await generator.revertFix(id)

    if (!success) {
      return res.status(404).json({ error: 'Fix not found or cannot be reverted' })
    }

    res.json({ message: 'Fix reverted successfully' })
  })
)