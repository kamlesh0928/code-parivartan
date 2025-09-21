import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def sanitize_filename(name):
    s = re.sub(r'[^a-zA-Z0-9_.-]', '', name).strip()
    return s[:100] if s else "file"

class LLMAgent:
    def __init__(self, name):
        self.name = name
    def generate_project_summary(self, context):
        raise NotImplementedError
    def generate_plan(self, summary, task):
        raise NotImplementedError
    def apply_changes(self, repo_path, plan, task):
        raise NotImplementedError

class GeminiAgent(LLMAgent):
    """An agent powered by Google Gemini, now capable of multi-file edits."""
    def __init__(self):
        super().__init__("Gemini")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "CRITICAL ERROR: GOOGLE_API_KEY not found. "
                "Please ensure you have a .env file in the project root "
                "and that it contains the correct GOOGLE_API_KEY."
            )
        print("[GeminiAgent] GOOGLE_API_KEY loaded successfully.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def _get_response(self, prompt):
        return self.model.generate_content(prompt).text

    def generate_project_summary(self, context):
        prompt = f"""
        Analyze this codebase and provide a concise summary of its purpose, language, and architecture.
        CODEBASE:
        {context[:30000]} 
        """
        return self._get_response(prompt)

    # --- MODIFIED: This now demands a structured JSON plan ---
    def generate_plan(self, summary, task):
        prompt = f"""
        You are an expert software architect. Based on the project summary and the user's task, identify all the files that need to be created or modified.
        Respond ONLY with a single JSON object. Do not add any text or markdown formatting before or after the JSON.
        The JSON object must have a single key "files_to_edit" which is a list of strings, where each string is a relative path to a file.

        SUMMARY: {summary}
        USER'S TASK: {task}

        Example Response:
        {{
          "files_to_edit": ["src/components/Login.js", "src/styles/main.css", "new_folder/new_file.py"]
        }}

        JSON RESPONSE:
        """
        response_text = self._get_response(prompt)
        try:
            # Clean the response to ensure it's a valid JSON object
            if response_text.strip().startswith("```json"):
                response_text = response_text.strip()[7:-3]
            plan_data = json.loads(response_text)
            if "files_to_edit" not in plan_data or not isinstance(plan_data["files_to_edit"], list):
                 raise KeyError("JSON must contain a 'files_to_edit' list.")
            return plan_data # Return the parsed JSON
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.name}] FAILED to parse the plan from LLM. Error: {e}")
            print(f"[{self.name}] Raw Response was:\n{response_text}")
            raise Exception("LLM did not return a valid JSON plan.")

    # --- MODIFIED: This now loops through the plan and executes on each file ---
    def apply_changes(self, repo_path, plan, task):
        """
        Parses the JSON plan and loops through each file, applying modifications.
        """
        print(f"[{self.name}] Now executing the multi-file plan...")
        files_to_edit = plan.get("files_to_edit", [])
        
        if not files_to_edit:
            raise ValueError("The AI's plan did not specify any files to edit.")

        print(f"[{self.name}] Plan involves modifying {len(files_to_edit)} file(s): {files_to_edit}")

        for target_file in files_to_edit:
            full_file_path = os.path.join(repo_path, target_file)
            
            # Determine if the file is new or needs modification
            is_new_file = not os.path.exists(full_file_path)
            original_content = ""

            if is_new_file:
                print(f"[{self.name}] Identified new file to create: {target_file}")
                # Ensure the directory exists before creating the file
                os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
            else:
                print(f"[{self.name}] Identified existing file to modify: {target_file}")
                with open(full_file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()

            # Construct the powerful "Executor" prompt for the current file
            execution_prompt = f"""
            You are an autonomous AI software engineer. Your task is to generate the complete, final content for a single file based on a user's request.

            USER's OVERALL TASK: "{task}"
            
            CURRENT FILE TO MODIFY: `{target_file}`
            {'This is a NEW FILE. Generate its content from scratch.' if is_new_file else ''}

            ORIGINAL FILE CONTENT of `{target_file}`:
            ---
            {original_content}
            ---

            You MUST respond ONLY with a single JSON object containing the new, complete content for the file `{target_file}`.
            Do not add any comments, explanations, or any text outside of the JSON object.

            Your response must be in the following JSON format:
            {{
              "file_path": "{target_file}",
              "new_content": "The full, updated content of the file, with all changes applied."
            }}
            """

            print(f"[{self.name}] Sending execution prompt to LLM for file: {target_file}...")
            response_text = self._get_response(execution_prompt)
            
            try:
                if response_text.strip().startswith("```json"):
                    response_text = response_text.strip()[7:-3]
                
                print(f"[{self.name}] Received response, parsing JSON for {target_file}...")
                data = json.loads(response_text)
                new_content = data["new_content"]
                
                print(f"[{self.name}] Writing updated content to {full_file_path}...")
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[{self.name}] Successfully wrote changes to {target_file}.")

            except (json.JSONDecodeError, KeyError) as e:
                print(f"[{self.name}] FAILED to process LLM response for {target_file}. Error: {e}")
                print(f"[{self.name}] Raw Response was:\n{response_text}")
                # Raise an exception to halt the process for this agent
                raise Exception(f"LLM returned invalid JSON for file {target_file}.")
        
        print(f"[{self.name}] Successfully completed all file modifications.")


def get_all_agents():
    """Returns a list of all configured agents."""
    agents = []
    try:
        agents.append(GeminiAgent())
    except ValueError as e:
        print(f"Could not initialize GeminiAgent: {e}")
    return agents

