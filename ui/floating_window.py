import tkinter as tk


class FloatingWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐞 Bug Vision")
        self.root.geometry("550x350+100+100")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#1e1e1e")

        # Header label
        self.header = tk.Label(
            self.root,
            text="🐞 Bug Vision — Watching your terminal...",
            bg="#1e1e1e",
            fg="#cccccc",
            font=("Consolas", 9),
            anchor="w",
            padx=8,
        )
        self.header.pack(fill=tk.X)

        # Main text area
        self.text_widget = tk.Text(
            self.root,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.text_widget.pack(expand=True, fill=tk.BOTH)

        # Queue for thread-safe updates
        self._pending_text = None

    def update_text(self, text: str):
        # Called from background thread — just store it, don't touch tkinter
        self._pending_text = text

    def _poll(self):
        # Called from main thread every 200ms — safe to update tkinter here
        if self._pending_text is not None:
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, self._pending_text)
            self._pending_text = None
        self.root.after(200, self._poll)

    def run(self):
        self._poll()  # Start the polling loop
        self.root.mainloop()