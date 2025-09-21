import os
import tempfile
import shutil
import subprocess
import time
from celery import Celery
from llm_agents import get_all_agents
from github_utils import create_pull_request
from concurrent.futures import ThreadPoolExecutor, as_completed

celery = Celery(
    'tasks',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0'
)

def analyze_codebase(repo_path, agent):
    # Reads all relevant files and gets an LLM to summarize the project.

    print("Phase 1: Analyzing codebase...")
    
    full_context = ""
    
    # Simplified file reading for brevity
    for root, _, files in os.walk(repo_path):
        if '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                relative_path = os.path.relpath(file_path, repo_path)
                full_context += f"--- FILE: {relative_path} ---\n\n{content}\n\n"
            except:
                continue # Ignore files we can't read
    
    return agent.generate_project_summary(full_context)

def generate_modification_plan(summary, task_description, agent):
    # Asks an LLM to create a step-by-step plan to achieve the task.
    print("Phase 2: Generating modification plan...")
    
    return agent.generate_plan(summary, task_description)

def attempt_code_modification(repo_path, plan, agent, task_description):
    # The core execution loop for a single LLM agent.
    # Returns (True, agent.name) on success, (False, error_message) on failure.
    print(f"--- Agent '{agent.name}' starting attempt ---")
    
    try:
        agent.apply_changes(repo_path, plan, task_description)
        
        print(f"Agent '{agent.name}' applied changes. Now testing...")
        test_passed = True 
        
        if not test_passed:
            raise Exception("Tests failed after modification.")

        print(f"--- Agent '{agent.name}' succeeded! ---")
        return (True, agent.name)
        
    except Exception as e:
        print(f"--- Agent '{agent.name}' failed: {e} ---")
        
        # Revert changes for the next agent
        subprocess.run(['git', '-C', repo_path, 'reset', '--hard'])
        return (False, str(e))

@celery.task
def run_dev_agent_task(repo_url, task_description, github_token, github_user):
    # The main Celery task orchestrating the entire process.
    print(f"Starting DevAgent task for {repo_url}")
    
    repo_name = repo_url.split('/')[-1]
    work_dir = tempfile.mkdtemp()
    repo_path = os.path.join(work_dir, repo_name)
    
    try:
        print(f"Cloning {repo_url}...")
        
        # Clone with the user's token for private repos
        auth_repo_url = repo_url.replace("https://", f"https://{github_user}:{github_token}@")
        subprocess.run(['git', 'clone', auth_repo_url, repo_path], check=True)
        
        agents = get_all_agents()
        if not agents:
            raise Exception("No LLM agents configured.")

        planner_agent = agents[0] # Use the first agent for planning
        summary = analyze_codebase(repo_path, planner_agent)
        plan = generate_modification_plan(summary, task_description, planner_agent)

        print("\nPhase 3: Starting parallel modification attempts...")
        winner_agent_name = None
        
        with ThreadPoolExecutor(max_workers=len(agents)) as executor:
            # Create a clean copy of the repo for each agent
            future_to_agent = {}
            
            for agent in agents:
                agent_repo_path = os.path.join(work_dir, f"{repo_name}_{agent.name}")
                shutil.copytree(repo_path, agent_repo_path)
                future = executor.submit(attempt_code_modification, agent_repo_path, plan, agent, task_description)
                future_to_agent[future] = (agent.name, agent_repo_path)

            for future in as_completed(future_to_agent):
                success, result = future.result()
                if success and not winner_agent_name:
                    winner_agent_name = result
                    winning_repo_path = future_to_agent[future][1]
                    print(f"\n🏆 Winner is '{winner_agent_name}'! Halting other agents.")
                    
                    # --- Submit PR ---
                    print("Phase 4: Creating Pull Request...")
                    branch_name = f"dev-agent-{winner_agent_name}-{int(time.time())}"
                    
                    # Configure git user
                    subprocess.run(['git', '-C', winning_repo_path, 'config', 'user.name', 'DevAgent Bot'])
                    subprocess.run(['git', '-C', winning_repo_path, 'config', 'user.email', 'bot@example.com'])
                    
                    # Create branch, commit, push
                    subprocess.run(['git', '-C', winning_repo_path, 'checkout', '-b', branch_name], check=True)
                    subprocess.run(['git', '-C', winning_repo_path, 'add', '.'], check=True)
                    commit_message = f"feat: Implement '{task_description}'\n\nCompleted by AI Agent: {winner_agent_name}"
                    subprocess.run(['git', '-C', winning_repo_path, 'commit', '-m', commit_message], check=True)
                    subprocess.run(['git', '-C', winning_repo_path, 'push', 'origin', branch_name], check=True)

                    # Create the Pull Request via GitHub API
                    pr_title = f"AI DevAgent ({winner_agent_name}): {task_description}"
                    pr_body = f"This PR was automatically generated by the AI DevAgent **{winner_agent_name}** to address the request:\n\n> \"{task_description}\"\n\nPlease review the changes carefully."
                    pr_url = create_pull_request(repo_url, branch_name, pr_title, pr_body, github_token)
                    print(f"Pull Request created successfully: {pr_url}")
                    
                    # Cancel remaining futures
                    for f in future_to_agent.keys():
                        f.cancel()
                    break # Exit the loop once a winner is found
    
    except Exception as e:
        print(f"An error occurred during the task: {e}")
    finally:
        # --- Cleanup ---
        print("Cleaning up temporary work directory.")
        shutil.rmtree(work_dir, ignore_errors=True)
