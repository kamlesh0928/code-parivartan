import requests
import json

def create_pull_request(repo_url, branch_name, title, body, token):
    """Creates a pull request on GitHub."""
    
    # Extract owner and repo name from URL
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo = parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    data = {
        "title": title,
        "body": body,
        "head": branch_name,
        "base": "main",
    }
    
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        return response.json()["html_url"]
    else:
        raise Exception(f"Failed to create PR: {response.status_code} - {response.text}")
