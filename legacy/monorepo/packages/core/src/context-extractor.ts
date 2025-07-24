import { promises as fs } from 'fs'
import path from 'path'

export interface CodeContext {
  file: string
  line: number
  function?: string
  class?: string
  code: string[]
  highlight: {
    start: number
    end: number
  }
}

export class ContextExtractor {
  async extractContext(
    filepath: string,
    lineNumber: number,
    contextSize: number = 15
  ): Promise<CodeContext> {
    try {
      const content = await fs.readFile(filepath, 'utf8')
      const lines = content.split('\n')
      
      // Find function and class boundaries
      const { functionName, className, funcStart, funcEnd } = this.findBoundaries(lines, lineNumber - 1)
      
      // Determine context range
      let startLine = Math.max(0, lineNumber - contextSize - 1)
      let endLine = Math.min(lines.length - 1, lineNumber + contextSize - 1)
      
      // Expand to include full function if possible
      if (funcStart !== -1 && funcEnd !== -1) {
        startLine = Math.max(0, funcStart)
        endLine = Math.min(lines.length - 1, funcEnd)
      }
      
      // Extract the code lines
      const codeLines = lines.slice(startLine, endLine + 1)
      
      return {
        file: filepath,
        line: lineNumber,
        function: functionName,
        class: className,
        code: codeLines,
        highlight: {
          start: lineNumber - startLine - 1,
          end: lineNumber - startLine - 1
        }
      }
    } catch (error) {
      console.error(`Failed to extract context from ${filepath}:`, error)
      return {
        file: filepath,
        line: lineNumber,
        code: [`Error reading file: ${error}`],
        highlight: { start: 0, end: 0 }
      }
    }
  }

  private findBoundaries(lines: string[], targetLine: number): {
    functionName?: string
    className?: string
    funcStart: number
    funcEnd: number
  } {
    let functionName: string | undefined
    let className: string | undefined
    let funcStart = -1
    let funcEnd = -1
    let braceCount = 0
    let inFunction = false
    
    // Scan backwards to find function/class start
    for (let i = targetLine; i >= 0; i--) {
      const line = lines[i]
      const trimmed = line.trim()
      
      // Check for class definition
      const classMatch = trimmed.match(/^\s*(?:class|struct)\s+(\w+)/)
      if (classMatch && !className) {
        className = classMatch[1]
      }
      
      // Check for function definition
      const funcMatch = this.matchFunctionSignature(line)
      if (funcMatch && !inFunction) {
        functionName = funcMatch
        funcStart = i
        inFunction = true
        braceCount = 0
      }
      
      // Count braces to find function boundaries
      if (inFunction) {
        for (const char of line) {
          if (char === '{') braceCount++
          if (char === '}') braceCount--
        }
        
        // If we've closed all braces, we've found the function start
        if (braceCount < 0) {
          funcStart = i + 1
          break
        }
      }
    }
    
    // Scan forward to find function end
    if (funcStart !== -1) {
      braceCount = 0
      let foundOpenBrace = false
      
      for (let i = funcStart; i < lines.length; i++) {
        const line = lines[i]
        
        for (const char of line) {
          if (char === '{') {
            braceCount++
            foundOpenBrace = true
          }
          if (char === '}') {
            braceCount--
          }
        }
        
        // Function ends when brace count returns to 0 after opening
        if (foundOpenBrace && braceCount === 0) {
          funcEnd = i
          break
        }
      }
    }
    
    return { functionName, className, funcStart, funcEnd }
  }

  private matchFunctionSignature(line: string): string | undefined {
    // Common C++ function patterns
    const patterns = [
      // Regular function: return_type function_name(params)
      /^\s*(?:(?:static|inline|virtual|explicit|constexpr)\s+)*(?:[\w:]+\s+)*(\w+)\s*\([^)]*\)\s*(?:const)?\s*(?:override)?\s*(?:noexcept)?\s*{?/,
      // Constructor/Destructor
      /^\s*(?:explicit\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*\w+[^{]*)?{?/,
      /^\s*~(\w+)\s*\([^)]*\)\s*(?:override)?\s*{?/,
      // Template function
      /^\s*template\s*<[^>]+>\s*(?:[\w:]+\s+)*(\w+)\s*\([^)]*\)/
    ]
    
    for (const pattern of patterns) {
      const match = line.match(pattern)
      if (match && match[1]) {
        // Filter out keywords that look like functions
        const keywords = ['if', 'while', 'for', 'switch', 'catch', 'return']
        if (!keywords.includes(match[1])) {
          return match[1]
        }
      }
    }
    
    return undefined
  }

  async extractMultipleContexts(
    contexts: Array<{ file: string; line: number }>,
    contextSize: number = 15
  ): Promise<CodeContext[]> {
    const results = await Promise.all(
      contexts.map(({ file, line }) => 
        this.extractContext(file, line, contextSize)
      )
    )
    
    return results
  }

  formatContextForDisplay(context: CodeContext): string {
    const lines: string[] = []
    
    // Add header
    lines.push(`File: ${context.file}`)
    if (context.class) {
      lines.push(`Class: ${context.class}`)
    }
    if (context.function) {
      lines.push(`Function: ${context.function}`)
    }
    lines.push('---')
    
    // Add code with line numbers
    const startLineNum = context.line - context.highlight.start
    context.code.forEach((codeLine, index) => {
      const lineNum = startLineNum + index
      const isHighlighted = index === context.highlight.start
      const prefix = isHighlighted ? '>' : ' '
      lines.push(`${prefix}${lineNum.toString().padStart(4)}: ${codeLine}`)
    })
    
    return lines.join('\n')
  }
}