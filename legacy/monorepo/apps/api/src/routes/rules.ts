import { Router } from 'express'
import { z } from 'zod'
import path from 'path'
import { promises as fs } from 'fs'
import { asyncHandler } from '../middleware/async'
import { validateRequest } from '../middleware/validate'

export const rulesRouter = Router()

const createRuleSchema = z.object({
  body: z.object({
    name: z.string(),
    description: z.string(),
    category: z.enum(['modernization', 'safety', 'performance', 'style']),
    pattern: z.string(),
    fix: z.string().optional(),
    enabled: z.boolean().optional()
  })
})

// Get all rules
rulesRouter.get(
  '/',
  asyncHandler(async (req, res) => {
    const rulesFile = path.join(process.cwd(), 'data', 'custom-rules.json')
    
    try {
      const data = await fs.readFile(rulesFile, 'utf8')
      const rules = JSON.parse(data)
      res.json(rules)
    } catch (error) {
      res.json([])
    }
  })
)

// Create custom rule
rulesRouter.post(
  '/',
  validateRequest(createRuleSchema),
  asyncHandler(async (req, res) => {
    const rule = req.body
    const rulesFile = path.join(process.cwd(), 'data', 'custom-rules.json')
    const dataDir = path.join(process.cwd(), 'data')

    // Ensure data directory exists
    await fs.mkdir(dataDir, { recursive: true })

    let rules = []
    try {
      const data = await fs.readFile(rulesFile, 'utf8')
      rules = JSON.parse(data)
    } catch (error) {
      // File doesn't exist yet
    }

    const newRule = {
      id: Date.now().toString(),
      ...rule,
      enabled: rule.enabled ?? true,
      createdAt: new Date().toISOString()
    }

    rules.push(newRule)
    await fs.writeFile(rulesFile, JSON.stringify(rules, null, 2))

    res.status(201).json(newRule)
  })
)

// Update rule
rulesRouter.put(
  '/:id',
  asyncHandler(async (req, res) => {
    const { id } = req.params
    const updates = req.body
    const rulesFile = path.join(process.cwd(), 'data', 'custom-rules.json')

    try {
      const data = await fs.readFile(rulesFile, 'utf8')
      const rules = JSON.parse(data)
      const index = rules.findIndex((r: any) => r.id === id)

      if (index === -1) {
        return res.status(404).json({ error: 'Rule not found' })
      }

      rules[index] = { ...rules[index], ...updates }
      await fs.writeFile(rulesFile, JSON.stringify(rules, null, 2))

      res.json(rules[index])
    } catch (error) {
      res.status(404).json({ error: 'Rule not found' })
    }
  })
)

// Delete rule
rulesRouter.delete(
  '/:id',
  asyncHandler(async (req, res) => {
    const { id } = req.params
    const rulesFile = path.join(process.cwd(), 'data', 'custom-rules.json')

    try {
      const data = await fs.readFile(rulesFile, 'utf8')
      const rules = JSON.parse(data)
      const filtered = rules.filter((r: any) => r.id !== id)

      if (filtered.length === rules.length) {
        return res.status(404).json({ error: 'Rule not found' })
      }

      await fs.writeFile(rulesFile, JSON.stringify(filtered, null, 2))
      res.json({ message: 'Rule deleted' })
    } catch (error) {
      res.status(404).json({ error: 'Rule not found' })
    }
  })
)

// Test rule
rulesRouter.post(
  '/test',
  asyncHandler(async (req, res) => {
    const { pattern, code } = req.body

    // Simple regex test for demonstration
    try {
      const regex = new RegExp(pattern, 'g')
      const matches = []
      let match

      while ((match = regex.exec(code)) !== null) {
        matches.push({
          text: match[0],
          index: match.index,
          line: code.substring(0, match.index).split('\n').length
        })
      }

      res.json({ matches, count: matches.length })
    } catch (error: any) {
      res.status(400).json({ error: error.message })
    }
  })
)