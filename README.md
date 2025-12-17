# Code Parivartan

Code Parivartan is an AI agent that functions on its own, comprehends, organizes, and carries out changes in the code of software repositories by user-friendly language instructions. 
It has the abilities of a software developer but virtually, that means, it can do everything from patching a software with a small error to implementing a set of complex features 
spanning several files, and so on.

---

## Vision

Code Parivartan's idea is to speed up the software development process through the efficient handling of the same coding tasks that are repetitive and time consuming by the user. 
The developers can hand off the minutiae that go into the code to the agent, thus freeing their creative minds for designing, making a breakthrough in problem solving, and 
innovating further. This initiative is a very strong indication of a future in which co-working between AI and human developers is effortless.

---

## Core Features

  - **Autonomous Code Analysis:** The agent imports the whole codebase and uses the large language model (LLM) to create a high level summary of the code's goal, language, and architecture.

  - **Intelligent Multi-file Planning:** The agent, before coding a single line, recognizes all the files to be created or changed to meet the user's request, and then, it makes a stepwise plan.

  - **Automated Code Generation:** The agent cleverly provides the LLM with the context of the existing code and then, for every file in his plan, he produces complete, updated content.

   - **Asynchronous Task Execution:** The agent, built on a solid architecture with Celery and Redis, which allow him to do complicated and long running tasks in the background without any interface blockage.

  - **Simple Web Interface:** A user-friendly and beautiful UI helps the users to easily drop a GitHub repo URL and a task to start the agent.

---

## How It Works: The Agent's Workflow

The agent executes a thorough, multi-step process to guarantee precision, and trustworthiness.

**1. Task Submission:** A user shares a public GitHub repository URL along with a general description of the task (e.g., "Add a dark mode toggle to the navbar").

**2. Code Ingestion:** The agent copies the repository that the user has pointed to a secure, temporary workspace on the server.

**3. Phase 1: Analysis:** The agent inspects the file structure and provides the Google Gemini with the codebase context to get a brief summary of the project.

**4. Phase 2: Planning:** The agent takes the project summary and the user’s task, then asks the LLM to come up with a strategic plan. One of the outputs is a JSON list containing all file paths that will be changed.

**5. Phase 3: Execution & Code Generation:** The agent gets the content of all files which have been identified in the plan. Next, to LLM, it sends the task together with the full content of these files as one final, comprehensive prompt. LLM reads this context and shares back in a structured JSON format the complete, updated code for each file.

**6. File System Modification:** The agent takes the output from the LLM and disassembles it to extract the updated portions of code. Subsequently, the code is written to the corresponding files in the temporary workspace, thus, the coding task is finished.

---

## Technology Stack

**Backend**

  - **Python:** The main programming language used for server side logic.

  - **Flask:** A simple web framework that was used to build the API and serve the frontend.

  - **Celery:** A distributed task queue for handling long running, asynchronous AI agent jobs.

  - **Redis:** An in-memory data store that serves as the message broker for Celery.

**AI Core**

  - **Google Gemini:** The generative AI model that serves as the core intelligence for code understanding, planning, and generation.

**Frontend**

  - **Next.js:** A React framework that is used for creating server rendered web applications of high performance. 

---

# Use Cases

The use of this project can be perfectly matched with the automation of software development processes that encompass:

  - **Rapid Feature Prototyping:** Growing the existing application with new features or components in a quick manner.

  - **Automated Bug Fixing:** Understanding the bug description and making an attempt to fix it by implementation.

  - **Code Refactoring:** Making changes that affect the whole repository such as upgrading dependencies or switching to a new API standard.

  - **Generating Boilerplate Code:** Creating new routes, models, or UI components that are in line with the template.

---

## Contributions
Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request.

---

## License
This project is licensed under the MIT License. Please see the [LICENSE](LICENSE) file for more information.

---

