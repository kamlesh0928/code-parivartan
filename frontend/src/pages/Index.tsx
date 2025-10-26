import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import {
  Rocket,
  Github,
  GitPullRequest,
  Clock,
  Sparkles,
  Users,
  FileCode,
  Clipboard,
  ArrowRight,
  Zap,
  Loader2,
} from "lucide-react";
import heroAiRobot from "@/assets/hero-ai-robot-4.jpg";

const SERVER_URL = import.meta.env.VITE_SERVER_URL || "http://localhost:8080";

const Index = () => {
  const [repoUrl, setRepoUrl] = useState("");
  const [goal, setGoal] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [jobId, setJobId] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(true); // Assume authenticated initially; backend will handle 401

  // Reference to the GitHub URL input section for scrolling
  const inputSectionRef = useRef(null);

  // Clear status message after 5 seconds
  useEffect(() => {
    if (statusMessage) {
      const timer = setTimeout(() => setStatusMessage(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [statusMessage]);

  const handleEnhancePrompt = async () => {
    if (!goal.trim()) {
      setStatusMessage("Please enter a modernization goal.");
      return;
    }

    setIsLoading(true);
    setStatusMessage("");
    try {
      const response = await axios.post(
        `${SERVER_URL}/api/enhance`,
        { prompt: goal },
        { withCredentials: true }
      );

      if (response.data.success && response.data.enhanced_prompt) {
        setGoal(response.data.enhanced_prompt);
        setStatusMessage("Prompt enhanced successfully!");
      } else {
        throw new Error("Invalid response from server");
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          setIsAuthenticated(false);
          setStatusMessage("Please log in to enhance your prompt.");
          return;
        }
        const errorMessage = error.response?.data?.error || "Failed to enhance prompt.";
        console.error("Error enhancing prompt:", error);
        setStatusMessage(`Error: ${errorMessage}`);
      } else {
        console.error("Unexpected error:", error);
        setStatusMessage(`Error: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!repoUrl.trim() || !goal.trim()) {
      setStatusMessage("Please provide both a repository URL and a modernization goal.");
      return;
    }

    setIsLoading(true);
    setStatusMessage("Submitting your task...");
    try {
      const response = await axios.post(
        `${SERVER_URL}/api/submit`,
        {
          repo_url: repoUrl,
          task_description: goal,
        },
        { withCredentials: true }
      );

      setJobId(response.data.job_id);
      setStatusMessage("Task submitted! Processing in progress...");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          setIsAuthenticated(false);
          setStatusMessage("Please log in to submit your task.");
          return;
        }
        const errorMessage = error.response?.data?.error || "Failed to submit task.";
        console.error("Error submitting task:", error);
        setStatusMessage(`Error: ${errorMessage}`);
      } else {
        console.error("Unexpected error:", error);
        setStatusMessage(`Error: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Poll task status
  useEffect(() => {
    if (!jobId) return;

    const pollStatus = async () => {
      try {
        const response = await axios.get(`${SERVER_URL}/api/task_status/${jobId}`, {
          withCredentials: true,
        });
        setStatusMessage(response.data.status);
        if (response.data.status === "SUCCESS" || response.data.status === "FAILURE") {
          if (response.data.result?.pr_url) {
            setStatusMessage(
              `<span>
                Task completed! View your{" "}
                <a href={response.data.result.pr_url} className="text-primary underline" target="_blank" rel="noopener noreferrer">
                  Pull Request
                </a>.
              </span>`
            );
          } else if (response.data.result?.message) {
            setStatusMessage(`Task failed: ${response.data.result.message}`);
          }
        } else {
          setTimeout(pollStatus, 5000);
        }
      } catch (error) {
        if (axios.isAxiosError(error)) {
          if (error.response?.status === 401) {
            setIsAuthenticated(false);
            setStatusMessage("Please log in to check task status.");
            return;
          }
          const errorMessage = error.response?.data?.error || "Failed to fetch task status.";
          console.error("Error polling task status:", error);
          setStatusMessage(`Error: ${errorMessage}`);
        } else {
          console.error("Unexpected error:", error);
          setStatusMessage(`Error: ${error.message}`);
        }
      }
    };

    pollStatus();
  }, [jobId]);

  const handleLogin = () => {
    window.location.href = `${SERVER_URL}/login`;
  };

  const handleGetStarted = () => {
    if (isAuthenticated) {
      inputSectionRef.current?.scrollIntoView({ behavior: "smooth" });
    } else {
      handleLogin();
    }
  };

  return (
    <main className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-background/80 border-b border-border transition-all duration-500 ease-in-out">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-8">
              <div className="text-3xl font-black glow-text transition-opacity duration-500">
                Code Parivartan
              </div>
            </div>
            <Button className="btn-login hover-glow" onClick={handleLogin}>
              Login with GitHub
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="pt-32 pb-16 px-6 animate-fade-in-up">
        <div className="container mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center min-h-[80vh]">
            <div className="space-y-8 text-center lg:text-left transition-all duration-700 ease-in-out">
              <div className="space-y-6">
                <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                  Elevate Your Code to
                  <br />
                  the <span className="glow-text">Next Level</span>
                  <Rocket className="inline-block w-12 h-12 ml-4 gradient-icon animate-float" />
                </h1>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto lg:mx-0">
                  Code Parivartan empowers you to write, debug, and scale code effortlessly with AI-driven insights. Transform your development workflow today.
                </p>
              </div>
              <div className="flex justify-center lg:justify-start mt-8">
                <Button className="btn-hero px-8 py-4 flex items-center space-x-2" onClick={handleGetStarted}>
                  <span>Get Started</span>
                  <ArrowRight className="w-5 h-5" />
                </Button>
              </div>
            </div>
            <div className="relative animate-scale-in-smooth">
              <div className="relative rounded-3xl overflow-hidden hero-image-glow inline-block">
                <img
                  src={heroAiRobot}
                  alt="AI Robot representing advanced code transformation"
                  className="w-auto h-auto max-w-full rounded-2xl"
                  loading="lazy"
                />
              </div>
              <div className="absolute -top-3 left-4 dancing-button bg-green-500/20 backdrop-blur-sm border border-green-500/40 px-4 py-2 rounded-full flex items-center space-x-2 z-20">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-green-400 font-semibold">AI Active</span>
              </div>
              <div className="absolute bottom-0 right-4 dancing-button bg-blue-500/20 backdrop-blur-sm border border-blue-500/40 px-4 py-2 rounded-full flex items-center space-x-2 z-20">
                <Zap className="w-4 h-4 text-blue-400" />
                <span className="text-blue-400 font-semibold">200% Productivity Boost</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Code Automation Section */}
      <section className="py-20 px-6 animate-fade-in-up" ref={inputSectionRef}>
        <div className="container mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold">
              Streamline Your <span className="glow-text">Code Modernization</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Input your repository and goal, and let Code Parivartan AI deliver a polished pull request with optimized, tested code in minutes.
            </p>
          </div>
          <div className="max-w-4xl mx-auto relative">
            <Card className="input-container-glow animate-fade-in-smooth">
              <CardContent className="space-y-6 p-8 relative">
                <div className="space-y-4">
                  <label className="text-lg font-semibold">GitHub Repository URL</label>
                  <Input
                    placeholder="e.g., https://github.com/username/repo"
                    value={repoUrl}
                    onChange={(e) => setRepoUrl(e.target.value)}
                    className={`bg-background border-border text-lg py-6 focus:ring-2 focus:ring-primary/50 transition-all duration-300 ${!isAuthenticated ? "blur-sm cursor-not-allowed" : ""}`}
                    disabled={isLoading || !isAuthenticated}
                  />
                </div>
                <div className="space-y-4">
                  <label className="text-lg font-semibold">Your Modernization Goal</label>
                  <Textarea
                    placeholder='e.g., "Convert JavaScript to TypeScript and remove unused callbacks"'
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    className={`bg-background border-border text-lg min-h-[120px] focus:ring-2 focus:ring-primary/50 transition-all duration-300 ${!isAuthenticated ? "blur-sm cursor-not-allowed" : ""}`}
                    disabled={isLoading || !isAuthenticated}
                  />
                  <Button
                    className="w-full text-base py-3 mt-3 transition-all duration-300"
                    onClick={handleEnhancePrompt}
                    disabled={isLoading || !isAuthenticated}
                  >
                    {isLoading ? (
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    ) : (
                      <Sparkles className="w-4 h-4 mr-2" />
                    )}
                    {isLoading ? "Enhancing..." : "Enhance Prompt"}
                  </Button>
                </div>
                <Button
                  className="w-full text-xl py-6 flex items-center justify-center transition-all duration-300"
                  onClick={handleSubmit}
                  disabled={isLoading || !isAuthenticated}
                >
                  {isLoading ? (
                    <Loader2 className="w-6 h-6 mr-3 animate-spin" />
                  ) : (
                    <Rocket className="w-6 h-6 mr-3" />
                  )}
                  {isLoading ? "Submitting..." : "Transform Code"}
                  <ArrowRight className="w-6 h-6 ml-3" />
                </Button>
                {statusMessage && (
                  <div className="text-center text-sm text-muted-foreground mt-4 animate-fade-in">
                    {statusMessage}
                  </div>
                )}
                {!isAuthenticated && (
                  <div className="absolute inset-0 backdrop-blur-md bg-white/10 flex flex-col items-center justify-center rounded-lg z-10 transition-all duration-300">
                    <p className="text-lg font-semibold text-gray-200 mb-4">Log in to unlock code transformation</p>
                    <Button onClick={handleLogin} className="px-6 py-3 hover:bg-primary/90 transition-all duration-300">
                      Login with GitHub
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="section-glow py-20 px-6 animate-fade-in-up">
        <div className="container mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold">How It Works</h2>
            <p className="text-xl text-muted-foreground">
              Upgrade your codebase in three simple steps
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Card className="feature-card hover-glow text-center animate-fade-in-smooth">
              <CardContent className="p-0">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mx-auto mb-6 transition-all duration-300">
                  <FileCode className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4 glow-text">Link Your Repository</h3>
                <p className="text-muted-foreground">
                  Provide your GitHub repository URL for secure code analysis by our AI.
                </p>
              </CardContent>
            </Card>
            <Card className="feature-card hover-glow text-center animate-fade-in-smooth">
              <CardContent className="p-0">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mx-auto mb-6 transition-all duration-300">
                  <Clipboard className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4 glow-text">Define Your Goal</h3>
                <p className="text-muted-foreground">
                  Specify your code improvement objectives in plain language.
                </p>
              </CardContent>
            </Card>
            <Card className="feature-card hover-glow text-center animate-fade-in-smooth">
              <CardContent className="p-0">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mx-auto mb-6 transition-all duration-300">
                  <GitPullRequest className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4 glow-text">Receive a Pull Request</h3>
                <p className="text-muted-foreground">
                  Get a comprehensive, AI-generated pull request ready for your review.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* AI Features Section */}
      <section id="features" className="section-glow py-20 px-6 animate-fade-in-up">
        <div className="container mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold">
              Advanced <span className="glow-text">AI Features</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Discover how Code Parivartan’s intelligent tools enhance your development experience
            </p>
          </div>
          <div className="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
            <Card className="feature-card hover-glow animate-fade-in-smooth text-center">
              <CardContent className="p-0 flex flex-col items-center">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mb-6 transition-all duration-300">
                  <Clock className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4">AI Debugging Assistant</h3>
                <p className="text-muted-foreground leading-relaxed text-center">
                  Instantly detect errors and receive automated fixes powered by advanced AI.
                </p>
              </CardContent>
            </Card>
            <Card className="feature-card hover-glow animate-fade-in-smooth text-center">
              <CardContent className="p-0 flex flex-col items-center">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mb-6 transition-all duration-300">
                  <Sparkles className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4">Smart Code Suggestions</h3>
                <p className="text-muted-foreground leading-relaxed text-center">
                  Get real-time code enhancements tailored to your project’s context.
                </p>
              </CardContent>
            </Card>
            <Card className="feature-card hover-glow animate-fade-in-smooth text-center">
              <CardContent className="p-0 flex flex-col items-center">
                <div className="w-16 h-16 rounded-3xl gradient-outline hover-glow flex items-center justify-center mb-6 transition-all duration-300">
                  <Users className="w-8 h-8 gradient-icon" />
                </div>
                <h3 className="text-2xl font-bold mb-4">Team Collaboration Tools</h3>
                <p className="text-muted-foreground leading-relaxed text-center">
                  Seamlessly integrate with your workflow to boost team productivity.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How Code Parivartan Works Section */}
      <section className="py-20 px-6 animate-fade-in-up">
        <div className="container mx-auto">
          <div className="text-center space-y-6 mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold">
              How <span className="glow-text">Code Parivartan</span> Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Transform your code in minutes with our streamlined process
            </p>
          </div>
          <div className="flex flex-col lg:flex-row items-center justify-center space-y-8 lg:space-y-0 lg:space-x-8">
            <div className="text-center space-y-4 animate-fade-in-smooth">
              <div className="w-20 h-20 rounded-3xl gradient-outline flex items-center justify-center mx-auto shadow-2xl transition-all duration-300">
                <span className="text-2xl font-bold text-white">01</span>
              </div>
              <h3 className="text-xl font-bold">Connect Your Codebase</h3>
              <p className="text-muted-foreground max-w-xs text-sm leading-relaxed">
                Easily integrate Code Parivartan with your development environment.
              </p>
            </div>
            <div className="flex items-center">
              <div className="w-8 h-0.5 gradient-border hidden lg:block"></div>
              <div className="w-4 h-4 rounded-full bg-gradient-primary mx-2 hidden lg:block"></div>
              <ArrowRight className="w-6 h-6 gradient-icon mx-2 animated-arrow" />
              <div className="w-4 h-4 rounded-full bg-gradient-primary mx-2 hidden lg:block"></div>
              <div className="w-8 h-0.5 gradient-border hidden lg:block"></div>
            </div>
            <div className="text-center space-y-4 animate-fade-in-smooth">
              <div className="w-20 h-20 rounded-3xl gradient-outline flex items-center justify-center mx-auto shadow-2xl transition-all duration-300">
                <span className="text-2xl font-bold text-white">02</span>
              </div>
              <h3 className="text-xl font-bold">AI-Powered Analysis</h3>
              <p className="text-muted-foreground max-w-xs text-sm leading-relaxed">
                Our AI instantly evaluates your code for improvements and optimizations.
              </p>
            </div>
            <div className="flex items-center">
              <div className="w-8 h-0.5 gradient-border hidden lg:block"></div>
              <div className="w-4 h-4 rounded-full bg-gradient-primary mx-2 hidden lg:block"></div>
              <ArrowRight className="w-6 h-6 gradient-icon mx-2 animated-arrow" />
              <div className="w-4 h-4 rounded-full bg-gradient-primary mx-2 hidden lg:block"></div>
              <div className="w-8 h-0.5 gradient-border hidden lg:block"></div>
            </div>
            <div className="text-center space-y-4 animate-fade-in-smooth">
              <div className="w-20 h-20 rounded-3xl gradient-outline flex items-center justify-center mx-auto shadow-2xl transition-all duration-300">
                <span className="text-2xl font-bold text-white">03</span>
              </div>
              <h3 className="text-xl font-bold">Smart Recommendations</h3>
              <p className="text-muted-foreground max-w-xs text-sm leading-relaxed">
                Receive tailored suggestions to enhance code quality and performance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-card/50 border-t border-border/50 animate-fade-in-up">
        <div className="max-w-7xl mx-auto px-4 py-16">
          <div className="text-center space-y-6">
            <div className="text-4xl font-bold glow-text">Code Parivartan</div>
            <div className="w-10 h-10 footer-icon-outline flex items-center justify-center mx-auto transition-all duration-300">
              <Github className="w-5 h-5" />
            </div>
            <div className="text-3xl font-bold text-white">
              by Code Hammer
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
};

export default Index;