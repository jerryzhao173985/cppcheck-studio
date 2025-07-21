import chalk from 'chalk'
import ora from 'ora'
import open from 'open'
import portfinder from 'portfinder'
import { spawn } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export async function startCommand(options: any) {
  const spinner = ora('Starting CPPCheck Studio...').start()

  try {
    // Find available port
    const port = await portfinder.getPortPromise({
      port: parseInt(options.port),
      stopPort: parseInt(options.port) + 100
    })

    if (port !== parseInt(options.port)) {
      spinner.info(`Port ${options.port} is busy, using port ${port}`)
    }

    // Set environment variables
    const env = {
      ...process.env,
      PORT: port.toString(),
      API_PORT: (port + 1).toString()
    }

    if (options.project) {
      env.DEFAULT_PROJECT_PATH = options.project
    }

    // Start the web server
    const webPath = path.resolve(__dirname, '../../../apps/web')
    const webProcess = spawn('npm', ['run', 'dev'], {
      cwd: webPath,
      env,
      stdio: 'pipe'
    })

    // Start the API server
    const apiPath = path.resolve(__dirname, '../../../apps/api')
    const apiProcess = spawn('npm', ['run', 'dev'], {
      cwd: apiPath,
      env: { ...env, PORT: env.API_PORT },
      stdio: 'pipe'
    })

    // Handle process output
    webProcess.stdout?.on('data', (data) => {
      if (data.toString().includes('ready')) {
        spinner.succeed(chalk.green(`CPPCheck Studio is running at http://localhost:${port}`))
        
        if (options.open) {
          open(`http://localhost:${port}`)
        }
      }
    })

    webProcess.stderr?.on('data', (data) => {
      console.error(chalk.red('Web Error:'), data.toString())
    })

    apiProcess.stderr?.on('data', (data) => {
      console.error(chalk.red('API Error:'), data.toString())
    })

    // Handle shutdown
    const shutdown = () => {
      console.log(chalk.yellow('\nShutting down CPPCheck Studio...'))
      webProcess.kill()
      apiProcess.kill()
      process.exit(0)
    }

    process.on('SIGINT', shutdown)
    process.on('SIGTERM', shutdown)

    // Keep process alive
    process.stdin.resume()

  } catch (error: any) {
    spinner.fail(chalk.red(`Failed to start: ${error.message}`))
    process.exit(1)
  }
}