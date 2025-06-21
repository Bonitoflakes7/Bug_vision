import time
import threading
from llm.bug_fixer import explain_error
from ocr.screen_reader import capture_screen, extract_text
from ui.floating_window import FloatingWindow
from config import CAPTURE_INTERVAL

def run_loop(window):
    while True:
        try:
            print("\n[🔁] LOOP STARTING...")
            response = ""
            display = "✅ No bug detected."

            img_path = capture_screen()
            print("[📸] Screenshot taken:", img_path)

            text = extract_text(img_path)
            print("[🧾] OCR Result:\n", text[:300])

            if "Traceback" in text or "Error" in text or "Exception" in text:
                print("[⚠] Bug detected! Sending to Mistral...")
                response = explain_error(text)

                if response:
                    print("[✅] Got response:\n", response[:300])
                    display = f"🪲 Error:\n{text[:300]}\n\n🛠 Fix:\n{response}"
                else:
                    print("[❌] Mistral gave no response.")
                    display = "⚠ Bug detected, but no fix returned."
            else:
                print("[✅] No error found on screen.")

        except Exception as e:
            print("[💥] Loop crashed:", e)
            display = f"💥 Crash in loop:\n{e}\n\n🧠 Last response:\n{response or '[no reply]'}"

        print("[📤] Updating floating window...")
        window.update_text(display)

        time.sleep(CAPTURE_INTERVAL)

def main():
    print("[🚀] Starting Live Bug Explainer...")

    window = FloatingWindow()

    t = threading.Thread(target=run_loop, args=(window,))
    t.daemon = True
    t.start()

    print("[🪟] Running floating window GUI...")
    window.run()

if __name__ == "__main__":
    main()
