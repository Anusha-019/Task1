import tkinter as tk
from tkinter import messagebox
import json
import matplotlib.pyplot as plt
from datetime import datetime

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        tk.Label(root, text="BMI Calculator", font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(root, text="Weight (kg):", font=("Arial", 10)).pack()
        self.weight_entry = tk.Entry(root, width=20, font=("Arial", 10))
        self.weight_entry.pack(pady=5)

        tk.Label(root, text="Height (m):", font=("Arial", 10)).pack()
        self.height_entry = tk.Entry(root, width=20, font=("Arial", 10))
        self.height_entry.pack(pady=5)

        self.calculate_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
        self.calculate_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

        self.history_button = tk.Button(root, text="View History", command=self.view_history, font=("Arial", 10), bg="#2196F3", fg="white")
        self.history_button.pack(pady=5)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if height <= 0:
                raise ValueError("Height must be greater than 0.")
            bmi = round(weight / (height ** 2), 2)
            category = self.categorize_bmi(bmi)
            self.result_label.config(text=f"BMI: {bmi} ({category})")
            self.save_bmi_data(bmi)
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def save_bmi_data(self, bmi):
        data = {"bmi": bmi, "date": datetime.now().isoformat()}
        try:
            with open("bmi_history.json", "a") as file:
                file.write(json.dumps(data) + "\n")
            messagebox.showinfo("Success", "BMI data saved!")
        except IOError:
            messagebox.showerror("File Error", "Could not save data")

    def view_history(self):
        try:
            with open("bmi_history.json", "r") as file:
                data = [json.loads(line) for line in file]
            if data:
                dates = [datetime.fromisoformat(entry["date"]) for entry in data]
                bmi_values = [entry["bmi"] for entry in data]

                plt.figure(figsize=(10, 5))
                plt.plot(dates, bmi_values, marker="o", linestyle="-", color="teal")
                plt.xlabel("Date")
                plt.ylabel("BMI")
                plt.title("BMI History Over Time")
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()
                plt.show()
            else:
                messagebox.showinfo("History", "No BMI data found.")
        except IOError:
            messagebox.showerror("File Error", "Could not load data")

root = tk.Tk()
app = BMICalculatorApp(root)

root.geometry("400x300")

root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()
