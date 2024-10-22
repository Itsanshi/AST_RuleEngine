import tkinter as tk
from tkinter import messagebox
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

class RuleEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rule Engine GUI")
        self.root.configure(bg="#f2f2f2")  # Set background color

        # Define style settings
        label_font = ("Helvetica", 12, "bold")
        entry_font = ("Helvetica", 10)
        button_font = ("Helvetica", 10, "bold")
        button_bg = "#4CAF50"  # Green button
        button_fg = "#FFFFFF"  # White text
        entry_bg = "#FFFFFF"
        entry_fg = "#000000"

        # Create Rule
        self.create_rule_frame = tk.Frame(root, bg="#f2f2f2")
        self.create_rule_frame.pack(pady=10)
        tk.Label(self.create_rule_frame, text="Create Rule", font=label_font, bg="#f2f2f2").pack()
        self.rule_string_entry = tk.Entry(self.create_rule_frame, width=50, font=entry_font, bg=entry_bg, fg=entry_fg)
        self.rule_string_entry.pack(pady=5)
        self.create_rule_button = tk.Button(self.create_rule_frame, text="Create Rule", font=button_font, bg=button_bg, fg=button_fg, command=self.create_rule)
        self.create_rule_button.pack(pady=5)

        # Combine Rules
        self.combine_rule_frame = tk.Frame(root, bg="#f2f2f2")
        self.combine_rule_frame.pack(pady=10)
        tk.Label(self.combine_rule_frame, text="Combine Rules (comma-separated IDs)", font=label_font, bg="#f2f2f2").pack()
        self.rule_ids_entry = tk.Entry(self.combine_rule_frame, width=50, font=entry_font, bg=entry_bg, fg=entry_fg)
        self.rule_ids_entry.pack(pady=5)
        self.combine_rule_button = tk.Button(self.combine_rule_frame, text="Combine Rules", font=button_font, bg=button_bg, fg=button_fg, command=self.combine_rules)
        self.combine_rule_button.pack(pady=5)

        # Evaluate Rule
        self.evaluate_rule_frame = tk.Frame(root, bg="#f2f2f2")
        self.evaluate_rule_frame.pack(pady=10)
        tk.Label(self.evaluate_rule_frame, text="Evaluate Rule (Mega Rule ID)", font=label_font, bg="#f2f2f2").pack()
        self.mega_rule_id_entry = tk.Entry(self.evaluate_rule_frame, width=50, font=entry_font, bg=entry_bg, fg=entry_fg)
        self.mega_rule_id_entry.pack(pady=5)
        tk.Label(self.evaluate_rule_frame, text="Data (JSON)", font=label_font, bg="#f2f2f2").pack()
        self.data_entry = tk.Entry(self.evaluate_rule_frame, width=50, font=entry_font, bg=entry_bg, fg=entry_fg)
        self.data_entry.pack(pady=5)
        self.evaluate_rule_button = tk.Button(self.evaluate_rule_frame, text="Evaluate Rule", font=button_font, bg=button_bg, fg=button_fg, command=self.evaluate_rule)
        self.evaluate_rule_button.pack(pady=5)

        # Modify Rule
        self.modify_rule_frame = tk.Frame(root, bg="#f2f2f2")
        self.modify_rule_frame.pack(pady=10)
        tk.Label(self.modify_rule_frame, text="Modify Rule ID", font=label_font, bg="#f2f2f2").pack()
        self.modify_rule_id_entry = tk.Entry(self.modify_rule_frame, width=50, font=entry_font, bg=entry_bg, fg=entry_fg)
        self.modify_rule_id_entry.pack(pady=5)
        tk.Label(self.modify_rule_frame, text="New Rule String", font=label_font, bg="#f2f2f2").pack()
        self.new_rule_string_entry = tk.Entry(self.modify_rule_frame, width=50, font=entry_font, bg=entry_bg, fg=entry_fg)
        self.new_rule_string_entry.pack(pady=5)
        self.modify_rule_button = tk.Button(self.modify_rule_frame, text="Modify Rule", font=button_font, bg=button_bg, fg=button_fg, command=self.modify_rule)
        self.modify_rule_button.pack(pady=5)

        # Output
        self.output_text = tk.Text(root, height=10, width=80, font=entry_font, bg=entry_bg, fg=entry_fg)
        self.output_text.pack(pady=10)

    def create_rule(self):
        rule_string = self.rule_string_entry.get()
        try:
            response = requests.post(f"{BASE_URL}/create_rule", json={"rule_string": rule_string})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Create Rule Response: {response.json()}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def combine_rules(self):
        rule_ids = self.rule_ids_entry.get().split(',')
        rule_ids = [int(id.strip()) for id in rule_ids]
        try:
            response = requests.post(f"{BASE_URL}/combine_rules", json={"rule_ids": rule_ids})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Combine Rules Response: {response.json()}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def evaluate_rule(self):
        mega_rule_id = int(self.mega_rule_id_entry.get())
        data = self.data_entry.get()
        try:
            data_json = json.loads(data)
            response = requests.post(f"{BASE_URL}/evaluate_rule", json={"rule_id": mega_rule_id, "data": data_json})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Evaluate Rule Response: {response.json()}\n")
        except json.JSONDecodeError as e:
            self.output_text.insert(tk.END, f"JSON Decode Error: {e}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def modify_rule(self):
        rule_id = int(self.modify_rule_id_entry.get())
        new_rule_string = self.new_rule_string_entry.get()
        try:
            response = requests.post(f"{BASE_URL}/modify_rule", json={"rule_id": rule_id, "new_rule_string": new_rule_string})
            response.raise_for_status()
            self.output_text.insert(tk.END, f"Modify Rule Response: {response.json()}\n")
        except requests.exceptions.RequestException as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RuleEngineApp(root)
    root.mainloop()
