from celery import Celery
from llm_agents import GeminiAgent
from github_utils import GitHubManager
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

def enhance_prompt(task_description):
    """Enhance the user-provided task description using Gemini API."""
    logger.info(f"Enhancing prompt: {task_description}")
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-pro")
        prompt_instruction = f"""
        You are an expert AI coding assistant. Enhance the provided prompt to be concise, specific, and actionable for an AI coding agent. Focus on clarity, include technical details (e.g., data models, API contracts, best practices), and ensure timezone-aware logic where relevant. Respond only with the enhanced prompt as a string.

        Original prompt: "{task_description}"

        Example enhanced prompt:
        Implement a backend feature to track user daily streaks for completing tasks via POST /api/v1/tasks. Store current_streak (INTEGER, default 0) and last_active_date (DATE) in the Users table. Increment streak if the task is completed on the consecutive day in the user's timezone; reset to 1 if two or more days are missed; do not increment for same-day tasks. Update GET /api/v1/users/me to include current_streak. Ensure atomic updates, optimize for performance, and include unit tests for all scenarios.
        """
        response = model.generate_content(prompt_instruction)
        enhanced_text = response.text.strip()
        logger.info(f"Enhanced prompt: {enhanced_text}")
        return enhanced_text
    except Exception as e:
        logger.error(f"Error enhancing prompt: {str(e)}", exc_info=True)
        raise

@app.task
def run_dev_agent_task(repo_url, task_description, github_token, github_user):
    logger.info(f"Starting task for repo: {repo_url}, task: {task_description}, user: {github_user}")
    
    try:
        # Enhance the task description
        enhanced_task = enhance_prompt(task_description)
        logger.info(f"Enhanced task description: {enhanced_task}")
        
        # Initialize the GitHub manager
        github_manager = GitHubManager(github_token)
        logger.info("GitHubManager initialized successfully")
        
        # Fork the repository
        fork_url = github_manager.fork_repository(repo_url)
        logger.info(f"Repository forked: {fork_url}")
        
        # Initialize the Gemini agent
        agent = GeminiAgent()
        logger.info("GeminiAgent initialized successfully")
        
        # Analyze and modify the repository
        modifications = agent.analyze_and_modify(fork_url, enhanced_task)
        logger.info(f"Modifications generated: {modifications}")
        
        # Create a branch and commit changes
        branch_name = f"ai-agent-task-{enhanced_task[:20].replace(' ', '-')}"
        github_manager.create_branch(fork_url, branch_name)
        logger.info(f"Branch created: {branch_name}")
        
        github_manager.commit_changes(fork_url, branch_name, modifications)
        logger.info(f"Changes committed to branch: {branch_name}")
        
        # Create a pull request
        pr_url = github_manager.create_pull_request(fork_url, branch_name, enhanced_task)
        logger.info(f"Pull Request created: {pr_url}")
        
        return {"status": "success", "pr_url": pr_url}
    
    except Exception as e:
        logger.error(f"Error in run_dev_agent_task: {str(e)}", exc_info=True)
        return {"status": "error", "message": str(e)}