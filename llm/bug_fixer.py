import requests
from config import OLLAMA_BASE_URL, LLM_MODEL

_last_sent_error: str = ""


def explain_error(error_text: str, context: str = "") -> str:
    """
    Send error_text to Mistral. If context is provided (retrieved
    code chunks from RAG), it's injected into the prompt so Mistral
    can give project-specific advice.
    """
    global _last_sent_error

    if error_text.strip() == _last_sent_error.strip():
        print("[⏭] Same error as last time, skipping.")
        return ""

    _last_sent_error = error_text.strip()

    # Build the prompt — context section is only included if RAG found something
    context_section = ""
    if context:
        context_section = f"""Here are the most relevant parts of the user's codebase:

{context}

"""

    prompt = f"""{context_section}You are a debugging assistant. Analyze the error below and respond with:
1. A one-line summary of what went wrong
2. The likely root cause (reference specific function/variable names if visible in the code above)
3. The exact fix with a short code snippet if applicable

Error from terminal:
{error_text}
"""

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )

        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            print(f"[❌] HTTP Error: {response.status_code}")
            return ""

    except requests.exceptions.ConnectionError:
        print("[❌] Ollama not reachable. Run: ollama serve")
        return ""
    except Exception as e:
        print(f"[❌] Unexpected error: {e}")
        return ""