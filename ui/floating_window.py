
import tkinter as tk

class FloatingWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🐞 Bug Explainer")
        self.root.geometry("500x300+100+100")
        self.root.attributes("-topmost", True)

        self.text_widget = tk.Text(self.root, wrap=tk.WORD, font=("Consolas", 10))
        self.text_widget.pack(expand=True, fill=tk.BOTH)

    def update_text(self, text):
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, text)

    def run(self):
        self.root.mainloop()
