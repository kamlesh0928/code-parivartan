from flask import Flask, request, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from tasks import run_dev_agent_task
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from celery.result import AsyncResult

load_dotenv()

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={r"/*": {"origins": os.getenv("CLIENT_URL")}}
)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key-for-dev")
app.config.from_mapping(
    CELERY_BROKER_URL="redis://127.0.0.1:6379/0",
    CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/0",
)
app.celery_app = run_dev_agent_task.app

# GitHub OAuth Configuration
oauth = OAuth(app)
github = oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "repo"},
)

@app.route("/login")
def login():
    """Initialize GitHub OAuth login."""
    
    redirect_uri = url_for("authorize", _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    """Handle GitHub OAuth callback and store user info."""
    
    token = github.authorize_access_token()
    resp = github.get("user", token=token)
    resp.raise_for_status()
    user_info = resp.json()
    
    session["user"] = user_info["login"]
    session["github_token"] = token["access_token"]
    
    return redirect(os.getenv("CLIENT_URL"))

@app.route("/logout")
def logout():
    """Clear session and logout user."""
    
    session.pop("user", None)
    session.pop("github_token", None)
    return redirect(os.getenv("CLIENT_URL"))

@app.route("/api/submit", methods=["POST"])
def submit():
    """Submit a task to the AI agent via Celery."""
    
    if "user" not in session:
        return jsonify({"error": "Authentication required. Please log in."}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    repo_url = data.get("repo_url")
    task_description = data.get("task_description")
    
    if not repo_url or not task_description:
        return jsonify({"error": "Repository URL and task description are required."}), 400

    job = run_dev_agent_task.delay(
        repo_url, task_description, session["github_token"], session["user"]
    )
    
    return jsonify({
        "message": "Task submitted successfully!",
        "job_id": job.id,
        "status": "The agent is now working on it and will create a PR upon completion."
    }), 200

@app.route("/api/task_status/<job_id>", methods=["GET"])
def task_status(job_id):
    """Check the status of a Celery task."""
    
    try:
        task = AsyncResult(job_id, app=app.celery_app)
        if task.state == "PENDING":
            return jsonify({"status": "PENDING", "message": "Task is still processing"})
        elif task.state == "SUCCESS":
            return jsonify({"status": "SUCCESS", "result": task.result})
        elif task.state == "FAILURE":
            return jsonify({"status": "FAILURE", "result": task.result})
        else:
            return jsonify({"status": task.state, "message": "Task in unknown state"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/enhance", methods=["POST"])
def enhance_prompt():
    """Enhance a user-provided prompt using Gemini API."""
    
    try:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-pro")
        
        data = request.get_json()
        user_prompt = data.get("prompt")
        if not user_prompt:
            return jsonify({"error": "Prompt is missing from the request."}), 400

        prompt_instruction = f"""
        You are an expert AI coding assistant. Enhance the provided prompt to be concise, specific, and actionable for an AI coding agent. Focus on clarity, include technical details (e.g., data models, API contracts, best practices), and ensure timezone-aware logic where relevant. **Do not include any introductory text, explanations, headings, or additional sections.** Respond **only** with a valid JSON object containing a single key, `enhanced_prompt`, with the enhanced prompt as a string.

        Original prompt: "{user_prompt}"

        Example response:
        {{
          "enhanced_prompt": "Implement a backend feature to track user daily streaks for completing tasks via POST /api/v1/tasks. Store current_streak (INTEGER, default 0) and last_active_date (DATE) in the Users table. Increment streak if the task is completed on the consecutive day in the user's timezone; reset to 1 if two or more days are missed; do not increment for same-day tasks. Update GET /api/v1/users/me to include current_streak. Ensure atomic updates, optimize for performance, and include unit tests for all scenarios."
        }}

        JSON RESPONSE:
        """
        response = model.generate_content(prompt_instruction)
        response_text = response.text.strip()

        # Handle JSON response
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        try:
            data = json.loads(response_text)
            if "enhanced_prompt" not in data:
                raise KeyError("Response must contain 'enhanced_prompt' key")
            return jsonify({
                "success": True,
                "enhanced_prompt": data["enhanced_prompt"]
            }), 200
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing Gemini response: {e}, Raw: {response_text}")
            return jsonify({
                "success": False,
                "message": "Invalid response format from AI model",
                "error": str(e)
            }), 500

    except Exception as e:
        print(f"Error in enhance_prompt: {e}")
        return jsonify({
            "success": False,
            "message": "An error occurred during prompt enhancement.",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)