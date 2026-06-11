# Copyright (c) 2026 Leo
# Licensed under the ScrapeNFill Community License

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, scrolledtext, ttk

from core.process import Process


class App:
    def __init__(self, root, config):

        self.config = config
        self.cv = Process(config)

        self.root = root
        self.root.title("Mijn Process GUI")
        self.root.geometry("700x500")

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variables
        self.input_dir = tk.StringVar(value=config["DIRECTORIES"]["input"])
        self.output_dir = tk.StringVar(value=config["DIRECTORIES"]["output"])

        # ===== Input directory =====
        input_frame = ttk.Frame(root, padding=10)
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="Input directory:").pack(anchor="w")

        input_row = ttk.Frame(input_frame)
        input_row.pack(fill="x", pady=5)

        ttk.Entry(input_row, textvariable=self.input_dir).pack(side="left", fill="x", expand=True)

        ttk.Button(input_row, text="Browse...", command=self.select_input_dir).pack(
            side="left", padx=5
        )

        # ===== Output directory =====
        output_frame = ttk.Frame(root, padding=10)
        output_frame.pack(fill="x")

        ttk.Label(output_frame, text="Output directory:").pack(anchor="w")

        output_row = ttk.Frame(output_frame)
        output_row.pack(fill="x", pady=5)

        ttk.Entry(output_row, textvariable=self.output_dir).pack(side="left", fill="x", expand=True)

        ttk.Button(output_row, text="Browse...", command=self.select_output_dir).pack(
            side="left", padx=5
        )

        # ===== Start button =====
        button_frame = ttk.Frame(root, padding=10)
        button_frame.pack(fill="x")

        self.start_button = ttk.Button(
            button_frame, text="Start process", command=self.start_process
        )
        self.start_button.pack(anchor="e")

        # ===== Logging console =====
        log_frame = ttk.Frame(root, padding=10)
        log_frame.pack(fill="both", expand=True)

        ttk.Label(log_frame, text="Logging:").pack(anchor="w")

        self.log_console = scrolledtext.ScrolledText(log_frame, height=20, state="disabled")
        self.log_console.pack(fill="both", expand=True)

    def on_closing(self):
        self.config["DIRECTORIES"]["input"] = self.input_dir.get()
        self.config["DIRECTORIES"]["output"] = self.output_dir.get()
        with open("../config.ini", "w") as configfile:
            self.config.write(configfile)
        self.root.destroy()

    def select_input_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.input_dir.set(directory)

    def select_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def log(self, message):
        self.log_console.configure(state="normal")
        self.log_console.insert(tk.END, message + "\n")
        self.log_console.see(tk.END)
        self.log_console.configure(state="disabled")

    def start_process(self):
        input_dir = self.input_dir.get()
        output_dir = self.output_dir.get()
        template = self.config["TEMPLATE"]["template"]

        if not input_dir or not output_dir:
            self.log("ERROR: Selecteer input en output directory")
            return

        # Disable knop tijdens run
        self.start_button.config(state="disabled")

        # Run process in aparte thread zodat GUI responsive blijft
        thread = threading.Thread(
            target=self.run_process, args=(input_dir, output_dir, template), daemon=True
        )
        thread.start()

    def run_process(self, input_dir, output_dir, template):
        try:
            Path(output_dir).mkdir(exist_ok=True)

            for file in Path(input_dir).iterdir():
                if not file.is_file():
                    continue

                self.log(f"➡️ Processing {file.name}")

                cv_text = self.cv.extract_text(file)
                if not cv_text.strip():
                    self.log("⚠️ Geen tekst gevonden")
                    continue

                data = self.cv.cv_to_json(cv_text)
                if not data:
                    continue

                output_path = Path(output_dir) / f"{file.stem}.docx"
                self.cv.save_docx(data, template, output_path)

                self.log(f"✅ Saved: {output_path}")

        except Exception as e:
            self.log(f"FOUT: {e}")

        finally:
            self.start_button.config(state="normal")


def run(config, args):

    root = tk.Tk()
    app = App(root, config)
    if args.input:
        app.input_dir.set(args.input)
    if args.output:
        app.output_dir.set(args.output)
    #    if args.template:
    #        app.template_file.set(args.template)
    root.mainloop()
