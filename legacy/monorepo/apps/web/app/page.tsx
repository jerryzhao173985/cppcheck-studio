import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { FileCode2, GitBranch, Zap, Shield } from 'lucide-react'
import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-primary/20 to-background">
        <div className="container mx-auto px-4 py-24">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-primary to-blue-400 bg-clip-text text-transparent">
              CPPCheck Studio
            </h1>
            <p className="text-xl text-muted-foreground mb-8">
              Professional C++ static analysis with interactive fixes, beautiful diffs, and one-click improvements
            </p>
            <div className="flex gap-4 justify-center">
              <Link href="/analyze">
                <Button size="lg" className="gap-2">
                  <FileCode2 className="w-5 h-5" />
                  Start Analysis
                </Button>
              </Link>
              <Link href="/demo">
                <Button size="lg" variant="outline" className="gap-2">
                  <GitBranch className="w-5 h-5" />
                  View Demo
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-16">
            Enterprise-Grade Features
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard
              icon={<FileCode2 className="w-8 h-8" />}
              title="Smart Code Analysis"
              description="Powered by cppcheck with enhanced C++17/20 modernization rules and deep code understanding"
            />
            <FeatureCard
              icon={<GitBranch className="w-8 h-8" />}
              title="Interactive Diff Viewer"
              description="GitHub-style side-by-side diffs with syntax highlighting and one-click fix application"
            />
            <FeatureCard
              icon={<Zap className="w-8 h-8" />}
              title="Real-Time Fixes"
              description="See fixes instantly with dry-run preview, confidence scoring, and automatic backups"
            />
            <FeatureCard
              icon={<Shield className="w-8 h-8" />}
              title="Safe & Reliable"
              description="Every fix is validated, backed up, and reversible with complete audit trail"
            />
            <FeatureCard
              icon={<FileCode2 className="w-8 h-8" />}
              title="VS Code Integration"
              description="Seamless integration with your favorite editor for inline fixes and analysis"
            />
            <FeatureCard
              icon={<GitBranch className="w-8 h-8" />}
              title="CI/CD Ready"
              description="GitHub Actions, GitLab CI, and Jenkins plugins for automated quality gates"
            />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-24 bg-muted/50">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary mb-2">10K+</div>
              <div className="text-muted-foreground">Issues Fixed</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2">50+</div>
              <div className="text-muted-foreground">Fix Patterns</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2">95%</div>
              <div className="text-muted-foreground">Fix Accuracy</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary mb-2">100%</div>
              <div className="text-muted-foreground">Open Source</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <Card className="max-w-4xl mx-auto p-12 text-center bg-gradient-to-r from-primary/10 to-blue-500/10">
            <h2 className="text-3xl font-bold mb-4">
              Ready to improve your C++ code?
            </h2>
            <p className="text-xl text-muted-foreground mb-8">
              Get started in minutes with our powerful analysis tools
            </p>
            <div className="flex gap-4 justify-center">
              <Link href="/analyze">
                <Button size="lg">Start Free Analysis</Button>
              </Link>
              <Link href="/docs">
                <Button size="lg" variant="outline">Read Documentation</Button>
              </Link>
            </div>
          </Card>
        </div>
      </section>
    </main>
  )
}

function FeatureCard({ icon, title, description }: {
  icon: React.ReactNode
  title: string
  description: string
}) {
  return (
    <Card className="p-6 hover:shadow-lg transition-shadow">
      <div className="text-primary mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-muted-foreground">{description}</p>
    </Card>
  )
}