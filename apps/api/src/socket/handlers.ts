import { Server, Socket } from 'socket.io'
import { logger } from '../lib/logger'

interface AnalysisUpdate {
  analysisId: string
  progress: number
  status: 'running' | 'completed' | 'failed'
  filesProcessed: number
  totalFiles: number
  issues?: any[]
  error?: string
}

export const createSocketHandlers = (io: Server) => {
  io.on('connection', (socket: Socket) => {
    logger.info(`Client connected: ${socket.id}`)

    // Join analysis room
    socket.on('join-analysis', (analysisId: string) => {
      socket.join(`analysis:${analysisId}`)
      logger.info(`Socket ${socket.id} joined analysis:${analysisId}`)
    })

    // Leave analysis room
    socket.on('leave-analysis', (analysisId: string) => {
      socket.leave(`analysis:${analysisId}`)
    })

    // Join project room
    socket.on('join-project', (projectId: string) => {
      socket.join(`project:${projectId}`)
    })

    // Request analysis status
    socket.on('get-analysis-status', async (analysisId: string) => {
      // Emit current status
      socket.emit('analysis-status', {
        analysisId,
        status: 'running',
        progress: 50,
        filesProcessed: 25,
        totalFiles: 50
      })
    })

    // Handle disconnection
    socket.on('disconnect', () => {
      logger.info(`Client disconnected: ${socket.id}`)
    })
  })

  // Helper function to emit analysis updates
  const emitAnalysisUpdate = (update: AnalysisUpdate) => {
    io.to(`analysis:${update.analysisId}`).emit('analysis-update', update)
  }

  // Helper function to emit project updates
  const emitProjectUpdate = (projectId: string, data: any) => {
    io.to(`project:${projectId}`).emit('project-update', data)
  }

  // Export helpers for use in other parts of the app
  return {
    emitAnalysisUpdate,
    emitProjectUpdate
  }
}