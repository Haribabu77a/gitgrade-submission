Project Name: GitGrade - AI Repository Auditor
Description: GitGrade is an intelligent tool designed to help developers improve their code quality. It utilizes Google Gemini AI to analyze GitHub repositories, score their engineering standards, and generate a personalized roadmap for improvement. Built specifically for the GitGrade Hackathon.
Features:
Instant Analysis: Scans repository file structures and README content.
Engineering Score: Generates a quality score (0-100) based on best practices.
Actionable Roadmap: Provides a step-by-step guide to improve the codebase (e.g., "Add CI/CD", "Improve Test Coverage").
AI-Powered: Uses Google Gemini Pro for deep context understanding.
Tech Stack:
Backend: Python, Flask
AI Engine: Google Gemini Pro (Generative AI)
Frontend: HTML5, CSS3, JavaScript
API: GitHub REST API
How it Works:
The user pastes a GitHub URL.
The system fetches the file structure and documentation using the GitHub API.
Google Gemini AI analyzes the project structure against engineering best practices.
The user receives a score and a tailored list of improvements.
How to Run Locally:
Clone the repository.
Install dependencies (flask, requests, google-generativeai).
Add your Gemini API Key to the app.py file.
Run "python app.py" and visit http://127.0.0.1:5000

The working video link : https://drive.google.com/file/d/1NfLnU2kZaRBJbRAGuis0KJa3ZEHgmmj3/view?usp=sharing
