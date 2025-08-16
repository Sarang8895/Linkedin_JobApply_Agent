# utils/llm_answer.py
import requests
import json
import subprocess

PERPLEXITY_API_KEY = "your API Key"  # Replace with your actual key

def query_ollama(question_text):
    """Query local Ollama model"""
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", question_text],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"⚠️ Ollama error: {e}")
    return None

def query_perplexity(question_text):
    """Query Perplexity API"""
    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "sonar-small-online",  # or sonar-medium if you want more accuracy
            "messages": [
                {"role": "system", "content": "Answer succinctly for job application forms."},
                {"role": "user", "content": question_text}
            ]
        }
        resp = requests.post("https://api.perplexity.ai/chat/completions", headers=headers, data=json.dumps(data))
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"⚠️ Perplexity error: {e}")
    return None

def get_llm_answer(question_text, input_type="text"):
    """
    Get a smart answer based on question and input type.
    input_type can be: 'text', 'number', 'select'
    """
    # Pre-check for common cases
    q = question_text.lower()

    if "current salary CTC" in q:
        return "25"
    if "expected salary CTC" in q:
        return "40"    
    if "years" in q and "experience" in q:
        return "8"
    if "authorization" in q:
        return "Yes"
    if "relocate" in q:
        return "Yes"
    if "notice period" in q:
        return "30"

    if "location" in q:
        return "Bengaluru, Karnataka, India"    

    # Ask LLM (Ollama → Perplexity fallback)
    answer = query_ollama(question_text)
    if not answer:
        answer = query_perplexity(question_text)

    # Type-specific formatting
    if input_type == "number":
        # Extract number from answer or fallback
        import re
        match = re.search(r"\d+", answer or "")
        return match.group(0) if match else "0"
    elif input_type == "select":
        # Simplify for dropdowns — often Yes/No or short strings
        if "yes" in (answer or "").lower():
            return "Yes"
        if "no" in (answer or "").lower():
            return "No"
        return "Yes"  # default
    else:
        return answer or "Yes"
