import os
import time
import threading
from llm.bug_fixer import explain_error
from ocr.screen_reader import capture_screen, extract_text
from ui.floating_window import FloatingWindow
from rag.indexer import index_codebase
from rag.retriever import load_vectorstore, retrieve_context
from config import CAPTURE_INTERVAL


def run_loop(window: FloatingWindow, vectorstore):
    while True:
        try:
            print("\n[🔁] Capturing screen...")

            img_path = capture_screen()
            text = extract_text(img_path)
            print(f"[🧾] OCR ({len(text)} chars): {text[:200]!r}")

            if any(kw in text for kw in ("Traceback", "Error", "Exception", "SyntaxError")):
                print("[⚠] Error detected — retrieving context...")

                # RAG: find relevant code from the indexed codebase
                context = ""
                if vectorstore:
                    context = retrieve_context(vectorstore, text)
                    if context:
                        print(f"[🔍] Retrieved {len(context)} chars of context")
                    else:
                        print("[🔍] No relevant context found in index")

                print("[🤖] Querying Mistral...")
                response = explain_error(text, context=context)

                if response:
                    context_note = "📎 (with your codebase context)" if context else "📎 (no codebase indexed)"
                    display = (
                        f"🪲 Detected Error {context_note}:\n"
                        f"{text[:400]}\n\n"
                        f"{'─' * 40}\n\n"
                        f"🛠 Fix:\n{response}"
                    )
                else:
                    display = "⏭ Same error as before — no new query sent."
            else:
                display = "✅ No errors detected on screen."

            window.update_text(display)

        except Exception as e:
            print(f"[💥] Loop error: {e}")
            window.update_text(f"💥 Internal error:\n{e}")

        time.sleep(CAPTURE_INTERVAL)


def main():
    print("[🚀] Bug Vision starting...")

    # ── RAG Setup ───────────────────────────────────────────────
    # Ask the user which project to index (or skip)
    project_path = input(
        "\n[📂] Enter path to your project folder to index (or press Enter to skip): "
    ).strip()

    vectorstore = None

    if project_path and os.path.isdir(project_path):
        # Index the codebase (safe to re-run — overwrites old index)
        index_codebase(project_path)
        vectorstore = load_vectorstore()
        print("[✅] RAG ready — Mistral will use your codebase as context")
    else:
        print("[⚠] No project indexed — running without RAG context")

    # ── Start loop ──────────────────────────────────────────────
    window = FloatingWindow()

    thread = threading.Thread(
        target=run_loop,
        args=(window, vectorstore),
        daemon=True,
    )
    thread.start()

    print(f"[ℹ] Watching screen every {CAPTURE_INTERVAL}s. Close the window to stop.")
    window.run()


if __name__ == "__main__":
    main()