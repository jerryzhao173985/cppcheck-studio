import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import compression from 'compression'
import { createServer } from 'http'
import { Server } from 'socket.io'
import { logger } from './lib/logger'
import { errorHandler } from './middleware/error'
import { createAnalysisRouter } from './routes/analysis'
import { createProjectRouter } from './routes/projects'
import { createFixRouter } from './routes/fixes'

const app = express()
const httpServer = createServer(app)
const io = new Server(httpServer, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true,
  },
})

// Middleware
app.use(helmet())
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true,
}))
app.use(compression())
app.use(express.json({ limit: '50mb' }))
app.use(express.urlencoded({ extended: true }))

// Routes
app.use('/api/analysis', createAnalysisRouter(io))
app.use('/api/projects', createProjectRouter())
app.use('/api/fixes', createFixRouter())

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// Error handling
app.use(errorHandler)

// WebSocket handling
io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}`)

  socket.on('join-project', (projectId: string) => {
    socket.join(`project:${projectId}`)
    logger.info(`Client ${socket.id} joined project ${projectId}`)
  })

  socket.on('leave-project', (projectId: string) => {
    socket.leave(`project:${projectId}`)
    logger.info(`Client ${socket.id} left project ${projectId}`)
  })

  socket.on('disconnect', () => {
    logger.info(`Client disconnected: ${socket.id}`)
  })
})

const PORT = process.env.PORT || 3001

httpServer.listen(PORT, () => {
  logger.info(`API server running on port ${PORT}`)
})