import requests

def explain_error(error_text):
    prompt = f"""
You are a helpful assistant that explains Python bugs.

Please explain this Python error and suggest how to fix it in 3 short bullet points:

{error_text}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code == 200:
            json_data = response.json()
            print("[📥] Mistral Raw Response:", json_data)  # ✅ debug
            return json_data.get("response", "").strip()
        else:
            print("[❌] HTTP Error:", response.status_code, response.text)
            return ""

    except Exception as e:
        print("[❌] Connection Error:", str(e))
        return ""

if __name__ == "__main__":
    test_error = "Traceback (most recent call last):\n  File 'main.py', line 2, in <module>\n    x = 1 / 0\nZeroDivisionError: division by zero"
    print("[🧪] Testing Mistral locally with error:")
    print(test_error)
    print("\n[📤] Sending to Mistral...\n")
    result = explain_error(test_error)
    print("\n[📥] Response from Mistral:\n", result)
