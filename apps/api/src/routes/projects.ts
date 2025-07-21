import { Router } from 'express'
import { z } from 'zod'
import path from 'path'
import { promises as fs } from 'fs'
import { asyncHandler } from '../middleware/async'
import { validateRequest } from '../middleware/validate'
import { logger } from '../lib/logger'

export const projectRouter = Router()

const createProjectSchema = z.object({
  body: z.object({
    name: z.string(),
    path: z.string(),
    profile: z.string().optional(),
    config: z.record(z.any()).optional()
  })
})

// Get all projects
projectRouter.get(
  '/',
  asyncHandler(async (req, res) => {
    const projectsFile = path.join(process.cwd(), 'data', 'projects.json')
    
    try {
      const data = await fs.readFile(projectsFile, 'utf8')
      const projects = JSON.parse(data)
      res.json(projects)
    } catch (error) {
      res.json([])
    }
  })
)

// Create new project
projectRouter.post(
  '/',
  validateRequest(createProjectSchema),
  asyncHandler(async (req, res) => {
    const { name, path: projectPath, profile = 'quick', config = {} } = req.body

    const projectsFile = path.join(process.cwd(), 'data', 'projects.json')
    const dataDir = path.join(process.cwd(), 'data')

    // Ensure data directory exists
    await fs.mkdir(dataDir, { recursive: true })

    let projects = []
    try {
      const data = await fs.readFile(projectsFile, 'utf8')
      projects = JSON.parse(data)
    } catch (error) {
      // File doesn't exist yet
    }

    const newProject = {
      id: Date.now().toString(),
      name,
      path: projectPath,
      profile,
      config,
      createdAt: new Date().toISOString(),
      lastAnalysis: null
    }

    projects.push(newProject)
    await fs.writeFile(projectsFile, JSON.stringify(projects, null, 2))

    res.status(201).json(newProject)
  })
)

// Get project by ID
projectRouter.get(
  '/:id',
  asyncHandler(async (req, res) => {
    const { id } = req.params
    const projectsFile = path.join(process.cwd(), 'data', 'projects.json')

    try {
      const data = await fs.readFile(projectsFile, 'utf8')
      const projects = JSON.parse(data)
      const project = projects.find((p: any) => p.id === id)

      if (!project) {
        return res.status(404).json({ error: 'Project not found' })
      }

      res.json(project)
    } catch (error) {
      res.status(404).json({ error: 'Project not found' })
    }
  })
)

// Update project
projectRouter.put(
  '/:id',
  asyncHandler(async (req, res) => {
    const { id } = req.params
    const updates = req.body
    const projectsFile = path.join(process.cwd(), 'data', 'projects.json')

    try {
      const data = await fs.readFile(projectsFile, 'utf8')
      const projects = JSON.parse(data)
      const index = projects.findIndex((p: any) => p.id === id)

      if (index === -1) {
        return res.status(404).json({ error: 'Project not found' })
      }

      projects[index] = { ...projects[index], ...updates }
      await fs.writeFile(projectsFile, JSON.stringify(projects, null, 2))

      res.json(projects[index])
    } catch (error) {
      res.status(404).json({ error: 'Project not found' })
    }
  })
)

// Delete project
projectRouter.delete(
  '/:id',
  asyncHandler(async (req, res) => {
    const { id } = req.params
    const projectsFile = path.join(process.cwd(), 'data', 'projects.json')

    try {
      const data = await fs.readFile(projectsFile, 'utf8')
      const projects = JSON.parse(data)
      const filtered = projects.filter((p: any) => p.id !== id)

      if (filtered.length === projects.length) {
        return res.status(404).json({ error: 'Project not found' })
      }

      await fs.writeFile(projectsFile, JSON.stringify(filtered, null, 2))
      res.json({ message: 'Project deleted' })
    } catch (error) {
      res.status(404).json({ error: 'Project not found' })
    }
  })
)