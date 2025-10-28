#!/usr/bin/env python3
"""
Base64 File Converter
A standalone utility to convert any file to Base64-encoded text.
- Select file → Convert → Copy to clipboard → Optional save
- Works with images, text, audio, binaries, etc.
- No external files. One .py file.
"""

import base64
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyperclip
import os
from pathlib import Path

class Base64ConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Base64 File Converter")
        self.root.geometry("760x560")
        self.root.minsize(600, 400)
        self.root.configure(bg="#f5f5f5")

        self.file_path = tk.StringVar()
        self.current_b64 = ""
        self.setup_ui()

    def setup_ui(self):
        # === Header ===
        header = tk.Label(
            self.root,
            text="Base64 File Converter",
            font=("Segoe UI", 18, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        header.pack(pady=(20, 10))

        subtitle = tk.Label(
            self.root,
            text="Convert any file to Base64 for embedding in code",
            font=("Segoe UI", 10),
            bg="#f5f5f5",
            fg="#7f8c8d"
        )
        subtitle.pack(pady=(0, 20))

        # === File Selection Frame ===
        file_frame = ttk.LabelFrame(self.root, text=" Input File ", padding=15)
        file_frame.pack(padx=30, pady=10, fill="x")

        path_entry = tk.Entry(
            file_frame,
            textvariable=self.file_path,
            font=("Consolas", 10),
            state="readonly",
            relief="sunken"
        )
        path_entry.pack(fill="x", pady=(0, 8))

        browse_btn = ttk.Button(
            file_frame,
            text="Browse File...",
            command=self.browse_file
        )
        browse_btn.pack()

        # === Action Frame ===
        action_frame = ttk.Frame(self.root)
        action_frame.pack(padx=30, pady=15, fill="x")

        self.convert_btn = ttk.Button(
            action_frame,
            text="Convert to Base64",
            command=self.convert_file,
            state="disabled"
        )
        self.convert_btn.pack(side="left", padx=(0, 10))

        self.copy_btn = ttk.Button(
            action_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            state="disabled"
        )
        self.copy_btn.pack(side="left", padx=(0, 10))

        self.save_btn = ttk.Button(
            action_frame,
            text="Save As...",
            command=self.save_base64,
            state="disabled"
        )
        self.save_btn.pack(side="left")

        # === Output Frame ===
        output_frame = ttk.LabelFrame(self.root, text=" Base64 Output ", padding=10)
        output_frame.pack(padx=30, pady=(10, 20), fill="both", expand=True)

        # Create text widget FIRST
        self.output_text = tk.Text(
            output_frame,
            font=("Consolas", 9),
            wrap="none",
            bg="#ffffff",
            fg="#2c3e50",
            relief="sunken",
            bd=1
        )

        # Now create scrollbars using self.output_text
        v_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        h_scroll = ttk.Scrollbar(output_frame, orient="horizontal", command=self.output_text.xview)
        self.output_text.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Grid layout
        self.output_text.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        # === Status Bar ===
        self.status = tk.Label(
            self.root,
            text="Select a file to begin",
            font=("Segoe UI", 9),
            bg="#ecf0f1",
            fg="#7f8c8d",
            anchor="w",
            padx=10
        )
        self.status.pack(fill="x", side="bottom")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File to Convert",
            filetypes=[
                ("All Files", "*.*"),
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("Text", "*.txt *.py *.json *.html *.css *.js"),
                ("Documents", "*.pdf *.docx *.xlsx"),
                ("Audio", "*.mp3 *.wav *.ogg"),
                ("Archives", "*.zip *.rar")
            ]
        )
        if file_path:
            self.file_path.set(file_path)
            self.convert_btn.config(state="normal")
            self.update_status(f"Ready: {os.path.basename(file_path)}")

    def convert_file(self):
        try:
            file_path = self.file_path.get()
            with open(file_path, "rb") as f:
                data = f.read()
            self.current_b64 = base64.b64encode(data).decode("utf-8")

            # Show in text box
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, self.current_b64)

            # Enable buttons
            self.copy_btn.config(state="normal")
            self.save_btn.config(state="normal")

            size_kb = len(data) / 1024
            self.update_status(f"Converted: {size_kb:.1f} KB → {len(self.current_b64)} characters")

        except Exception as e:
            messagebox.showerror("Conversion Error", f"Failed to read file:\n{str(e)}")

    def copy_to_clipboard(self):
        if self.current_b64:
            pyperclip.copy(self.current_b64)
            self.update_status("Copied to clipboard!")

    def save_base64(self):
        if not self.current_b64:
            return
        save_path = filedialog.asksaveasfilename(
            title="Save Base64 As",
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt"), ("All Files", "*.*")]
        )
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(self.current_b64)
                self.update_status(f"Saved: {os.path.basename(save_path)}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{str(e)}")

    def update_status(self, message):
        self.status.config(text=message)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    try:
        __import__("pyperclip")
    except ImportError:
        print("Installing required package: pyperclip")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
        print("pyperclip installed. Please run the script again.")
    else:
        app = Base64ConverterApp()
        app.run()