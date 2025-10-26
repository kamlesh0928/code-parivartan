import github
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubManager:
    def __init__(self, github_token):
        self.client = github.Github(github_token)
        logger.info("GitHub client initialized")

    def fork_repository(self, repo_url):
        try:
            repo_path = repo_url.replace("https://github.com/", "")
            repo = self.client.get_repo(repo_path)
            fork = repo.create_fork()
            logger.info(f"Forked repository: {fork.html_url}")
            return fork.html_url
        except Exception as e:
            logger.error(f"Error forking repository: {str(e)}")
            raise

    def create_branch(self, repo_url, branch_name):
        try:
            repo_path = repo_url.replace("https://github.com/", "")
            repo = self.client.get_repo(repo_path)
            source_branch = repo.get_branch("main")
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source_branch.commit.sha
            )
            logger.info(f"Created branch: {branch_name}")
        except Exception as e:
            logger.error(f"Error creating branch: {str(e)}")
            raise

    def commit_changes(self, repo_url, branch_name, modifications):
        try:
            repo_path = repo_url.replace("https://github.com/", "")
            repo = self.client.get_repo(repo_path)
            try:
                mods = json.loads(modifications)
                logger.info(f"Parsed {len(mods)} modifications")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse modifications as JSON: {str(e)}, Raw modifications: {modifications}")
                raise ValueError(f"Invalid JSON format in modifications: {str(e)}")

            for mod in mods:
                if not isinstance(mod, dict) or "file_path" not in mod or "content" not in mod:
                    logger.error(f"Invalid modification format: {mod}")
                    raise ValueError(f"Invalid modification format: {mod}")
                
                file_path = mod["file_path"]
                content = mod["content"]
                logger.info(f"Processing file: {file_path}")
                try:
                    file = repo.get_contents(file_path, ref=branch_name)
                    repo.update_file(
                        file_path,
                        f"Update {file_path} for task",
                        content,
                        file.sha,
                        branch=branch_name
                    )
                    logger.info(f"Updated file: {file_path}")
                except:
                    repo.create_file(
                        file_path,
                        f"Create {file_path} for task",
                        content,
                        branch=branch_name
                    )
                    logger.info(f"Created file: {file_path}")
            logger.info(f"Committed changes to {branch_name}")
        except Exception as e:
            logger.error(f"Error committing changes: {str(e)}")
            raise

    def create_pull_request(self, repo_url, branch_name, task_description):
        try:
            repo_path = repo_url.replace("https://github.com/", "")
            repo = self.client.get_repo(repo_path)
            pr = repo.create_pull(
                title=f"AI Agent: {task_description[:50]}",
                body=task_description,
                head=branch_name,
                base="main"
            )
            logger.info(f"Pull request created: {pr.html_url}")
            return pr.html_url
        except Exception as e:
            logger.error(f"Error creating pull request: {str(e)}")
            raise