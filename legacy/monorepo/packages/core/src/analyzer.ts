import { execa } from 'execa'
import { globby } from 'globby'
import PQueue from 'p-queue'
import * as path from 'node:path'
import * as fs from 'node:fs/promises'
import { CppcheckIssue, AnalysisConfig, AnalysisResult } from './types'
import { CppcheckParser } from './parser'
import { createHash } from './utils'

export class CppcheckAnalyzer {
  private parser: CppcheckParser
  private queue: PQueue

  constructor(private config: AnalysisConfig) {
    this.parser = new CppcheckParser()
    this.queue = new PQueue({ concurrency: config.threads || 4 })
    
    // Ensure paths are set if projectPath is provided
    if (config.projectPath && !config.paths) {
      this.config.paths = ['src', 'include', 'lib']
    }
  }

  async analyze(): Promise<AnalysisResult> {
    const startTime = Date.now()
    const files = await this.findFiles()
    
    const issues: CppcheckIssue[] = []
    const stats = {
      filesAnalyzed: 0,
      timeElapsed: 0,
      errors: 0,
      warnings: 0,
      style: 0,
      performance: 0,
      portability: 0,
      information: 0,
    }

    // Analyze files in batches
    const batches = this.createBatches(files, 50)
    
    await Promise.all(
      batches.map((batch) =>
        this.queue.add(async () => {
          try {
            const batchIssues = await this.analyzeBatch(batch)
            issues.push(...batchIssues)
            stats.filesAnalyzed += batch.length
          } catch (error) {
            console.error(`Failed to analyze batch:`, error)
            // Continue with other batches
          }
        })
      )
    )

    // Count issues by severity
    for (const issue of issues) {
      stats[issue.severity as keyof typeof stats]++
    }

    stats.timeElapsed = Date.now() - startTime

    return {
      issues,
      stats,
      profile: this.config.profile,
      timestamp: new Date().toISOString(),
    }
  }

  private async findFiles(): Promise<string[]> {
    const basePath = this.config.projectPath || process.cwd()
    const paths = this.config.paths || ['src', 'include', 'lib']
    
    const patterns = paths.map((p) => 
      path.join(basePath, p, '**/*.{cpp,cc,cxx,c++,hpp,h,hxx,h++}')
    )

    const files = await globby(patterns, {
      ignore: this.config.exclude || [],
      absolute: true,
    })

    return files
  }

  private createBatches<T>(items: T[], batchSize: number): T[][] {
    const batches: T[][] = []
    for (let i = 0; i < items.length; i += batchSize) {
      batches.push(items.slice(i, i + batchSize))
    }
    return batches
  }

  private async analyzeBatch(files: string[]): Promise<CppcheckIssue[]> {
    const args = this.buildCppcheckArgs(files)
    
    try {
      const { stdout, stderr } = await execa('cppcheck', args, {
        reject: false,
        maxBuffer: 50 * 1024 * 1024, // 50MB
      })

      const output = stderr || stdout
      return this.parser.parse(output)
    } catch (error) {
      console.error('Cppcheck analysis failed:', error)
      return []
    }
  }

  private buildCppcheckArgs(files: string[]): string[] {
    const args = [
      '--enable=' + this.getEnabledChecks(),
      '--std=c++17',
      '--template={file}:{line}:{column}: [{severity}:{id}] {message}',
      '--quiet',
      '--force',
      '--inline-suppr',
      `-j${this.config.threads || 4}`,
    ]

    // Add suppressions
    if (this.config.suppressions) {
      for (const suppression of this.config.suppressions) {
        args.push(`--suppress=${suppression}`)
      }
    }

    // Add include paths from the project
    const includeDirs = this.findIncludeDirs(files)
    for (const dir of includeDirs) {
      args.push(`-I${dir}`)
    }

    // Add files
    args.push(...files)

    return args
  }

  private getEnabledChecks(): string {
    const profileChecks: Record<string, string> = {
      quick: 'warning',
      full: 'all',
      cpp17: 'style,performance,portability',
      memory: 'warning',
      performance: 'performance',
    }

    return profileChecks[this.config.profile] || 'all'
  }

  private findIncludeDirs(files: string[]): Set<string> {
    const dirs = new Set<string>()
    
    for (const file of files) {
      const dir = path.dirname(file)
      const possibleIncludes = [
        path.join(dir, '..', 'include'),
        path.join(dir, '..', '..', 'include'),
        path.join(dir, 'include'),
      ]

      for (const includeDir of possibleIncludes) {
        if (await this.isDirectory(includeDir)) {
          dirs.add(includeDir)
        }
      }
    }

    return dirs
  }

  private async isDirectory(path: string): Promise<boolean> {
    try {
      const stat = await fs.stat(path)
      return stat.isDirectory()
    } catch {
      return false
    }
  }

  async getIncrementalFiles(cacheDir: string): Promise<string[]> {
    const allFiles = await this.findFiles()
    const changedFiles: string[] = []

    for (const file of allFiles) {
      const hash = await createHash(file)
      const cacheFile = path.join(cacheDir, `${hash}.json`)
      
      try {
        await fs.access(cacheFile)
        // File exists in cache, skip it
      } catch {
        // File not in cache or changed
        changedFiles.push(file)
      }
    }

    return changedFiles
  }
}