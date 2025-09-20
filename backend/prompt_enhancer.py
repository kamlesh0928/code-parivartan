# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for requests from your Next.js frontend

# Configure the Gemini API with your key from the environment variables
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Define the model to use
model = genai.GenerativeModel('gemini-pro')

@app.route('/api/enhance', methods=['POST'])
def enhance_prompt():
    """
    Receives a prompt, enhances it using the Gemini API, and returns the result.
    """
    try:
        # Get the JSON data from the incoming request
        data = request.get_json()
        user_prompt = data.get('prompt')

        # Check if a prompt was provided
        if not user_prompt:
            return jsonify({'error': 'Prompt is missing from the request.'}), 400

        # Construct the prompt for the Gemini model
        # The instruction tells the model what to do with the user's input.
        prompt_instruction = f"Enhance the following text to make it more professional, detailed, and engaging. The text is: {user_prompt}"

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
    # Run the Flask app
    app.run(debug=True, port=5000)