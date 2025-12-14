import os
import requests
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# CONFIGURATION
# GET A FREE GEMINI API KEY HERE: https://aistudio.google.com/app/apikey
# OR REPLACE WITH OPENAI LOGIC
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") # Optional but recommended for rate limits

if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)

def analyze_repo_with_ai(repo_url, files, readme_content):
    if not GENAI_API_KEY:
        return {"score": 50, "summary": "API Key Missing. Using default.", "roadmap": ["Add API Key"]}
    
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Act as a strict Senior Developer. Analyze this GitHub repository data:
    URL: {repo_url}
    Files: {files[:50]} (truncated)
    README Content (snippet): {readme_content[:1000]}

    OUTPUT A JSON OBJECT ONLY:
    {{
        "score": (integer 0-100),
        "summary": (string, max 2 sentences),
        "roadmap": (list of 3-5 actionable strings)
    }}
    """
    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it's valid JSON text
        clean_text = response.text.replace('```json', '').replace('```', '')
        return clean_text 
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    repo_url = data.get('url')
    
    # Extract owner/repo from URL (Simplistic)
    parts = repo_url.rstrip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'

    # 1. Fetch Repo Details
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    try:
        resp = requests.get(api_url, headers=headers)
        if resp.status_code != 200:
            return jsonify({"error": "Repo not found or private"}), 404
            
        repo_data = resp.json()
        file_names = [item['name'] for item in repo_data]
        
        # 2. Fetch Readme
        readme_content = ""
        if "README.md" in file_names:
            readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
            readme_content = requests.get(readme_url).text
        
        # 3. AI Analysis
        # If you don't have an AI Key yet, use this Mock Logic temporarily:
        # ai_result = {"score": 75, "summary": "Good start.", "roadmap": ["Fix Readme"]} 
        
        # Real AI Call (Uncomment if you have key):
        import json
        ai_response_text = analyze_repo_with_ai(repo_url, file_names, readme_content)
        ai_result = json.loads(ai_response_text)

        return jsonify(ai_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)