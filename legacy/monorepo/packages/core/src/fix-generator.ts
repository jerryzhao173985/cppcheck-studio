import { createTwoFilesPatch } from 'diff'
import { CppcheckIssue, CodeContext, FixSuggestion } from './types'

export class FixGenerator {
  private fixPatterns: Map<string, (issue: CppcheckIssue, context: CodeContext) => FixSuggestion | null>

  constructor() {
    this.fixPatterns = new Map([
      ['noExplicitConstructor', this.fixExplicitConstructor.bind(this)],
      ['missingOverride', this.fixMissingOverride.bind(this)],
      ['useNullptr', this.fixUseNullptr.bind(this)],
      ['passedByValue', this.fixPassedByValue.bind(this)],
      ['postfixOperator', this.fixPostfixOperator.bind(this)],
      ['unusedVariable', this.fixUnusedVariable.bind(this)],
      ['uninitMemberVar', this.fixUninitMember.bind(this)],
      ['uselessCallsCompare', this.fixUselessCompare.bind(this)],
    ])
  }

  generateFix(issue: CppcheckIssue, context: CodeContext): FixSuggestion | null {
    const fixFunction = this.fixPatterns.get(issue.id)
    if (!fixFunction) {
      return this.genericFix(issue, context)
    }

    return fixFunction(issue, context)
  }

  private fixExplicitConstructor(issue: CppcheckIssue, context: CodeContext): FixSuggestion {
    const targetLine = context.lines.find(l => l.isTarget)
    if (!targetLine) {
      return this.createFailedFix(issue, 'Target line not found')
    }

    const fixed = targetLine.content.replace(
      /(\s*)((?:inline\s+)?)([\w:]+)\s*\(/,
      '$1$2explicit $3('
    )

    return this.createFixSuggestion(
      issue,
      'Add explicit keyword to constructor',
      95,
      context,
      targetLine,
      fixed,
      'Single-parameter constructors should be marked explicit to prevent unintended implicit conversions.'
    )
  }

  private fixMissingOverride(issue: CppcheckIssue, context: CodeContext): FixSuggestion {
    const targetLine = context.lines.find(l => l.isTarget)
    if (!targetLine) {
      return this.createFailedFix(issue, 'Target line not found')
    }

    let fixed = targetLine.content
    if (targetLine.content.includes(';')) {
      fixed = targetLine.content.replace(/(\s*)(;)/, ' override$2')
    } else if (targetLine.content.includes('{')) {
      fixed = targetLine.content.replace(/(\s*)({)/, ' override $2')
    } else {
      fixed = targetLine.content.trimEnd() + ' override'
    }

    return this.createFixSuggestion(
      issue,
      'Add override specifier',
      98,
      context,
      targetLine,
      fixed,
      'Virtual functions that override base class methods should be marked with override for better type safety.'
    )
  }

  private fixUseNullptr(issue: CppcheckIssue, context: CodeContext): FixSuggestion {
    const targetLine = context.lines.find(l => l.isTarget)
    if (!targetLine) {
      return this.createFailedFix(issue, 'Target line not found')
    }

    let fixed = targetLine.content
    fixed = fixed.replace(/\bNULL\b/g, 'nullptr')
    fixed = fixed.replace(/(\w+\s*=\s*)0(\s*[;,)])/g, '$1nullptr$2')
    fixed = fixed.replace(/(\w+\()0(\))/g, '$1nullptr$2')
    fixed = fixed.replace(/(return\s+)0(\s*;)/g, '$1nullptr$2')

    return this.createFixSuggestion(
      issue,
      'Replace NULL/0 with nullptr',
      90,
      context,
      targetLine,
      fixed,
      'C++11 introduced nullptr as a type-safe null pointer constant. It should be used instead of NULL or 0.'
    )
  }

  private fixPassedByValue(issue: CppcheckIssue, context: CodeContext): FixSuggestion {
    const targetLine = context.lines.find(l => l.isTarget)
    if (!targetLine) {
      return this.createFailedFix(issue, 'Target line not found')
    }

    // Simple pattern for common cases
    const fixed = targetLine.content.replace(
      /(\b(?:std::)?(?:string|vector|map|set|list)\b)\s+(\w+)(\s*[,)])/g,
      'const $1& $2$3'
    )

    return this.createFixSuggestion(
      issue,
      'Pass by const reference',
      85,
      context,
      targetLine,
      fixed,
      'Large objects should be passed by const reference to avoid unnecessary copying.'
    )
  }

  private fixPostfixOperator(issue: CppcheckIssue, context: CodeContext): FixSuggestion {
    const targetLine = context.lines.find(l => l.isTarget)
    if (!targetLine) {
      return this.createFailedFix(issue, 'Target line not found')
    }

    let fixed = targetLine.content
    fixed = fixed.replace(/(\w+)\+\+/g, '++$1')
    fixed = fixed.replace(/(\w+)--/g, '--$1')

    return this.createFixSuggestion(
      issue,
      'Use prefix increment/decrement',
      90,
      context,
      targetLine,
      fixed,
      'Prefix increment/decrement is more efficient for non-primitive types as it avoids creating a temporary.'
    )
  }

  private fixUnusedVariable(issue: CppcheckIssue, context: CodeContext): FixSuggestion {
    const targetLine = context.lines.find(l => l.isTarget)
    if (!targetLine) {
      return this.createFailedFix(issue, 'Target line not found')
    }

    const indent = ' '.repeat(targetLine.indent)
    const fixed = `${indent}// ${targetLine.content.trim()} // UNUSED - TODO: Remove if not needed`

    return this.createFixSuggestion(
      issue,
      'Comment out unused variable',
      70,
      context,
      targetLine,
      fixed,
      'Unused variables should be removed to keep code clean. Commented out for review.',
      true
    )
  }

  private fixUninitMember(issue: CppcheckIssue, context: CodeContext): FixSuggestion | null {
    // This is complex and requires modifying the constructor
    return {
      id: `fix-${issue.id}-${Date.now()}`,
      issueId: issue.id,
      description: 'Initialize member variable in constructor',
      confidence: 60,
      diff: '',
      explanation: 'Member variables should be initialized in the constructor initializer list:\n\nMyClass() : member(0) { ... }',
      manualReview: true,
    }
  }

  private fixUselessCompare(issue: CppcheckIssue, context: CodeContext): FixSuggestion | null {
    return {
      id: `fix-${issue.id}-${Date.now()}`,
      issueId: issue.id,
      description: 'Fix string comparison',
      confidence: 75,
      diff: '',
      explanation: 'Use proper string comparison:\nif (str == "value") instead of if ("value")',
      manualReview: true,
    }
  }

  private genericFix(issue: CppcheckIssue, context: CodeContext): FixSuggestion | null {
    return {
      id: `fix-${issue.id}-${Date.now()}`,
      issueId: issue.id,
      description: `Fix ${issue.id}`,
      confidence: 50,
      diff: '',
      explanation: `Review and fix: ${issue.message}`,
      manualReview: true,
    }
  }

  private createFixSuggestion(
    issue: CppcheckIssue,
    description: string,
    confidence: number,
    context: CodeContext,
    targetLine: { number: number; content: string },
    fixedContent: string,
    explanation: string,
    manualReview = false
  ): FixSuggestion {
    // Create the diff
    const originalLines = context.lines.map(l => l.content)
    const fixedLines = [...originalLines]
    const targetIndex = context.lines.findIndex(l => l.number === targetLine.number)
    
    if (targetIndex !== -1) {
      fixedLines[targetIndex] = fixedContent
    }

    const diff = createTwoFilesPatch(
      context.file,
      context.file,
      originalLines.join('\n'),
      fixedLines.join('\n'),
      'original',
      'fixed'
    )

    return {
      id: `fix-${issue.id}-${Date.now()}`,
      issueId: issue.id,
      description,
      confidence,
      diff,
      explanation,
      manualReview,
    }
  }

  private createFailedFix(issue: CppcheckIssue, reason: string): FixSuggestion {
    return {
      id: `fix-${issue.id}-${Date.now()}`,
      issueId: issue.id,
      description: 'Fix generation failed',
      confidence: 0,
      diff: '',
      explanation: reason,
      manualReview: true,
    }
  }
}