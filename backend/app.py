import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from tasks import run_dev_agent_task
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {"origins": ["http://localhost:8080", "http://127.0.0.1:8080"]}
    }
)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key-for-dev")

app.config.from_mapping(
    CELERY_BROKER_URL='redis://127.0.0.1:6379/0',
    CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/0'
)

# GitHub Authentication/OAuth Configuration
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'repo'},
)

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    resp.raise_for_status()
    user_info = resp.json()
    
    # Store user info and token in session
    session['user'] = user_info['login']
    session['github_token'] = token['access_token']
    
    return redirect('http://localhost:8080/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('github_token', None)
    return redirect('http://localhost:8080/')

@app.route('/api/submit', methods=['POST'])
def submit():
    if 'user' not in session:
        return jsonify({"error": "Authentication required. Please log in."}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    repo_url = data.get('repo_url')
    task_description = data.get('task_description')
    
    if not repo_url or not task_description:
        return jsonify({"error": "Repository URL and task description are required."}), 400

    # Dispatch the long-running task to Celery
    job = run_dev_agent_task.delay(
        repo_url, 
        task_description, 
        session['github_token'],
        session['user']
    )
    
    return jsonify({
        "message": "Task submitted successfully!",
        "job_id": job.id,
        "status": "The agent is now working on it and will create a PR upon completion."
    }), 200

@app.route('/api/enhance', methods=['POST'])
def enhance_prompt():
    """
    Receives a prompt, enhances it using the Gemini API, and returns the result.
    """
    try:
        GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel('gemini-pro')
        
        # Get the JSON data from the incoming request
        data = request.get_json()
        user_prompt = data.get('prompt')

        # Check if a prompt was provided
        if not user_prompt:
            return jsonify({'error': 'Prompt is missing from the request.'}), 400

        prompt_instruction = f"Please enhance the following prompt to be more detailed and specific for code modernization: \"{user_prompt}\". Include suggestions for best practices, tools, and technologies that could be used."

        # Call the Gemini API to generate the enhanced content
        response = model.generate_content(prompt_instruction)
        enhanced_text = response.text

        # Return the enhanced text in a JSON response
        return jsonify({
            'success': True,
            'enhancedText': enhanced_text
        }), 200

    except Exception as e:
        # Catch any errors and return a clear error message
        return jsonify({
            'success': False,
            'message': 'An error occurred during prompt enhancement.',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)