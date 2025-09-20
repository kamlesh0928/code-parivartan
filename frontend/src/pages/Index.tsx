import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Rocket, 
  Github, 
  Target, 
  GitPullRequest, 
  Clock, 
  Sparkles, 
  Users, 
  FileCode, 
  Clipboard,
  ArrowRight,
  Zap,
  Bot,
  Instagram,
  MessageCircle,
  Facebook
} from 'lucide-react';

// X (formerly Twitter) icon as SVG component
const XIcon = ({ className }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="currentColor">
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
  </svg>
);

import heroCodeParivartan from '@/assets/hero-code-parivartan.jpg';

const Index = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [goal, setGoal] = useState('');

  return (
    <main className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-background/80 border-b border-border hover-glow">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-8">
              <div className="text-3xl font-black glow-text">Code Parivartan</div>
            </div>
            
            <button className="btn-login hover-glow">
              Login
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="pt-32 pb-16 px-6">
        <div className="container mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center min-h-[80vh]">
            <div className="space-y-8 animate-fade-in text-center lg:text-left">
              <div className="space-y-6">
                <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                  Transform Your Code to
                  <br />
                  the <span className="glow-text">Next Level</span>
                  <Rocket className="inline-block w-12 h-12 ml-4 gradient-icon animate-float" />
                </h1>
                
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto lg:mx-0">
                  Code Parivartan helps developers write, debug, and scale faster with AI-powered insights. Transform your development workflow with intelligent assistance.
                </p>
              </div>

            </div>

            <div className="relative animate-scale-in">
              <div className="glass-card p-8 rounded-3xl hero-image-glow">
                <img 
                  src={heroCodeParivartan} 
                  alt="Professional Code Transformation and Development" 
                  className="w-full h-auto rounded-2xl"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Code Automation Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold">
              Automate Your <span className="glow-text">Code Modernization</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Give Code Parivartan AI your repository and a goal. Get a pull request with modernized, 
              tested, and efficient code in minutes. No more manual refactoring.
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <div className="input-container-glow animate-fade-in">
              <CardContent className="space-y-6 p-0">
                <div className="space-y-4">
                  <div className="flex items-center justify-start space-x-3">
                    <label className="text-lg font-semibold">GitHub Repository URL</label>
                  </div>
                  <Input 
                    placeholder="https://github.com/your-org/repo-name"
                    value={repoUrl}
                    onChange={(e) => setRepoUrl(e.target.value)}
                    className="input-glow bg-secondary/50 border-border text-lg py-6"
                  />
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-start space-x-3">
                    <label className="text-lg font-semibold">Modernization Goal</label>
                  </div>
                  <Textarea 
                    placeholder='e.g., "Refactor all JavaScript files to use TypeScript and remove all dead callbacks"'
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    className="input-glow bg-secondary/50 border-border text-lg min-h-[120px]"
                  />
                  
                  <button className="btn-enhance w-full text-base py-3 mt-3">
                    <Sparkles className="w-4 h-4 mr-2 text-white" />
                    Enhance Your Prompt
                  </button>
                </div>

                <button className="btn-hero w-full text-xl py-6 flex items-center justify-center">
                  <Rocket className="w-6 h-6 mr-3" />
                  Transform My Code
                  <ArrowRight className="w-6 h-6 ml-3" />
                </button>
              </CardContent>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="section-glow py-20 px-6">
        <div className="container mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold">How It Works</h2>
            <p className="text-xl text-muted-foreground">
              Three simple steps to modernize your codebase
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="feature-card hover-glow text-center animate-fade-in">
              <CardContent className="p-0">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mx-auto mb-6">
                  <FileCode className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4 glow-text">Connect Your Repo</h3>
                <p className="text-muted-foreground">
                  Provide your GitHub repository URL. Code Parivartan AI will securely access and analyze your codebase.
                </p>
              </CardContent>
            </Card>

            <Card className="feature-card hover-glow text-center animate-fade-in">
              <CardContent className="p-0">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mx-auto mb-6">
                  <Clipboard className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4 glow-text">Define Your Goal</h3>
                <p className="text-muted-foreground">
                  Write a plain English prompt describing what you want to modernize or refactor in your code.
                </p>
              </CardContent>
            </Card>

            <Card className="feature-card hover-glow text-center animate-fade-in">
              <CardContent className="p-0">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mx-auto mb-6">
                  <GitPullRequest className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4 glow-text">Get a Pull Request</h3>
                <p className="text-muted-foreground">
                  Our AI agent analyzes, refactors, tests, and submits a comprehensive PR for your review.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* AI Features Section */}
      <section id="features" className="section-glow py-20 px-6">
        <div className="container mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold">
              Powerful <span className="glow-text">AI Features</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Discover how Code Parivartan's intelligent features transform your development experience
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            <Card className="feature-card hover-glow animate-fade-in text-center">
              <CardContent className="p-0 flex flex-col items-center">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mb-6">
                  <Clock className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4">AI Debugging Assistant</h3>
                <p className="text-muted-foreground leading-relaxed text-center">
                  Intelligent error detection and automated solutions powered by advanced machine learning algorithms.
                </p>
              </CardContent>
            </Card>

            <Card className="feature-card hover-glow animate-fade-in text-center">
              <CardContent className="p-0 flex flex-col items-center">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mb-6">
                  <Sparkles className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4">Smart Code Suggestions</h3>
                <p className="text-muted-foreground leading-relaxed text-center">
                  Real-time code completion and optimization recommendations that understand your project context.
                </p>
              </CardContent>
            </Card>

            <Card className="feature-card hover-glow animate-fade-in text-center">
              <CardContent className="p-0 flex flex-col items-center">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mb-6">
                  <Users className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4">Team Collaboration Tools</h3>
                <p className="text-muted-foreground leading-relaxed text-center">
                  Seamless integration with your workflow for enhanced team productivity and knowledge sharing.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How Code Parivartan Works Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold">
              How <span className="glow-text">Code Parivartan</span> Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Get started in minutes and transform your development workflow
            </p>
          </div>

          <div className="flex flex-col lg:flex-row items-center justify-center space-y-8 lg:space-y-0 lg:space-x-8">
            <div className="text-center space-y-4 animate-fade-in">
              <div className="w-20 h-20 rounded-3xl gradient-outline flex items-center justify-center mx-auto shadow-2xl">
                <span className="text-2xl font-bold gradient-icon">01</span>
              </div>
              <h3 className="text-xl font-bold">Connect Your Codebase</h3>
              <p className="text-muted-foreground max-w-xs text-sm leading-relaxed">
                Integrate Code Parivartan with your existing development environment in seconds.
              </p>
            </div>

            <div className="flex items-center">
              <div className="w-8 h-0.5 gradient-border hidden lg:block"></div>
              <ArrowRight className="w-6 h-6 gradient-icon mx-2" />
              <div className="w-8 h-0.5 gradient-border hidden lg:block"></div>
            </div>

            <div className="text-center space-y-4 animate-fade-in">
              <div className="w-20 h-20 rounded-3xl gradient-outline flex items-center justify-center mx-auto shadow-2xl">
                <span className="text-2xl font-bold gradient-icon">02</span>
              </div>
              <h3 className="text-xl font-bold">AI Analysis</h3>
              <p className="text-muted-foreground max-w-xs text-sm leading-relaxed">
                Our AI analyzes your code patterns, dependencies, and potential issues in real-time.
              </p>
            </div>

            <div className="flex items-center">
              <div className="w-8 h-0.5 gradient-border hidden lg:block"></div>
              <ArrowRight className="w-6 h-6 gradient-icon mx-2" />
              <div className="w-8 h-0.5 gradient-border hidden lg:block"></div>
            </div>

            <div className="text-center space-y-4 animate-fade-in">
              <div className="w-20 h-20 rounded-3xl gradient-outline flex items-center justify-center mx-auto shadow-2xl">
                <span className="text-2xl font-bold gradient-icon">03</span>
              </div>
              <h3 className="text-xl font-bold">Get Intelligent Insights</h3>
              <p className="text-muted-foreground max-w-xs text-sm leading-relaxed">
                Receive personalized recommendations to improve code quality and performance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-card/50 border-t border-border/50">
        <div className="max-w-7xl mx-auto px-4 py-16">
          <div className="text-center space-y-6">
            <div className="text-4xl font-bold glow-text">Code Parivartan</div>
            
            <div className="w-10 h-10 footer-icon-outline flex items-center justify-center mx-auto">
              <Github className="w-5 h-5" />
            </div>
            
            <div className="text-3xl font-bold text-white">by the code hammer</div>
          </div>
        </div>
      </footer>
    </main>
  );
};

export default Index;