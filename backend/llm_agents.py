import google.generativeai as genai
import os
import logging
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMAgent:
    def __init__(self, model_name):
        self.model_name = model_name

class GeminiAgent(LLMAgent):
    """An agent powered by Google Gemini for code analysis and modification."""
    
    def __init__(self):
        super().__init__("Gemini")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY not found in .env file.")
            raise ValueError("GOOGLE_API_KEY not found in .env file.")
        logger.info("GOOGLE_API_KEY loaded successfully")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-pro")
        logger.info("GeminiAgent model initialized")

    def analyze_and_modify(self, repo_url, task_description):
        logger.info(f"Analyzing repo: {repo_url} with task: {task_description}")
        try:
            prompt = f"""
            Analyze the repository at {repo_url} and generate code modifications to accomplish the following task:
            {task_description}
            **Return only a valid JSON array** containing file changes in the format:
            [
                {{
                    "file_path": "path/to/file",
                    "content": "new content of the file"
                }}
            ]
            **Do not include any introductory text, explanations, headings, or additional sections.** Respond **only** with the JSON array.
            """
            response = self.model.generate_content(prompt)
            logger.info("Gemini API response received")
            response_text = response.text.strip()

            # Fallback: Extract JSON array if response contains extra text
            json_match = re.search(r'\[\s*{.*?}\s*\]', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
                logger.info("Extracted JSON array from response")
            else:
                logger.warning("No JSON array found in response, attempting to parse as-is")

            # Validate JSON
            try:
                modifications = json.loads(response_text)
                if not isinstance(modifications, list):
                    raise ValueError("Response is not a JSON array")
                for mod in modifications:
                    if not isinstance(mod, dict) or "file_path" not in mod or "content" not in mod:
                        raise ValueError("Invalid modification format")
                logger.info("Validated JSON modifications")
                return json.dumps(modifications)  # Return as JSON string
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}, Raw response: {response_text}")
                raise ValueError(f"Invalid JSON response from Gemini API: {str(e)}")
            except ValueError as e:
                logger.error(f"Invalid modification format: {str(e)}, Raw response: {response_text}")
                raise
        except Exception as e:
            logger.error(f"Error in analyze_and_modify: {str(e)}", exc_info=True)
            raise