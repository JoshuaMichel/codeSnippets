# Given a path to an excel document of data, performs a series of transformations 
# specifically in excel and saves the file in the specified output
# Used Tkinter library to add a GUI user interface for user to 
# change the default input and output paths

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from automate_insights import perform_csv_transformation, get_last_sunday_date

# Set the default output folder
DEFAULT_OUTPUT_FOLDER = r"DEFAULT OUTPUT PATH HERE"

# Generate the default output file name using the get_last_sunday_date function
DEFAULT_OUTPUT_FILE_NAME = f"insights{get_last_sunday_date()}.xlsx"

# Combine the output folder and file name to get the default output file path
DEFAULT_OUTPUT_PATH = os.path.join(DEFAULT_OUTPUT_FOLDER, DEFAULT_OUTPUT_FILE_NAME)

class CSVTransformerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ITSD Insights App")

        # Set a green and white color theme
        self.bg_color = "#2ecc71"  # Green color
        self.button_bg_color = "white"
        self.button_fg_color = "#2c3e50"  # Dark gray color

        # Initialize variables
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()

        # Create GUI elements
        self.create_widgets()

        # Set a default value for output file path
        self.output_file_path.set(DEFAULT_OUTPUT_PATH)

    def create_widgets(self):
        # Set window size and padding
        self.root.geometry("600x400")
        self.root.configure(padx=20, pady=20, bg=self.bg_color)

        # Input File Selection
        tk.Label(self.root, text="Select Query Insights CSV File:", font=("Helvetica", 14), bg=self.bg_color, fg="white").pack()
        tk.Button(self.root, text="Browse", command=self.browse_input_file, font=("Helvetica", 12), bg=self.button_bg_color, fg=self.button_fg_color).pack()

        # Display selected file name
        self.selected_file_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg=self.bg_color, fg="white")
        self.selected_file_label.pack()

        # Output File Location
        tk.Label(self.root, text="Select Output Path:", font=("Helvetica", 14), bg=self.bg_color, fg="white").pack()
        tk.Entry(self.root, textvariable=self.output_file_path, state="readonly", font=("Helvetica", 12)).pack()

        # Add some vertical space
        tk.Frame(self.root, height=20, bg=self.bg_color).pack()

        tk.Button(self.root, text="Select Output Path", command=self.browse_output_location, font=("Helvetica", 12), bg=self.button_bg_color, fg=self.button_fg_color).pack()

        # Add more vertical space
        tk.Frame(self.root, height=20, bg=self.bg_color).pack()

        # Transform Button
        tk.Button(self.root, text="Create Insights", command=self.transform, font=("Helvetica", 14), bg=self.button_bg_color, fg=self.button_fg_color).pack()

        # Add more vertical space
        tk.Frame(self.root, height=20, bg=self.bg_color).pack()

        # Quit Button
        tk.Button(self.root, text="Quit", command=self.root.quit, font=("Helvetica", 14), bg=self.button_bg_color, fg=self.button_fg_color).pack()

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.input_file_path.set(file_path)
            self.update_selected_file_label(file_path)

    def browse_output_location(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_file_path.set(os.path.join(folder_path, "output.xlsx"))

    def transform(self):
        input_path = self.input_file_path.get()
        output_path = self.output_file_path.get()

        if not input_path or not os.path.isfile(input_path):
            messagebox.showerror("Error", "Please select a valid input CSV file.")
            return

        try:
            # Call the transformation function
            perform_csv_transformation(input_path, output_path)
            messagebox.showinfo("Success", f"Transformation complete. Result saved to: {output_path}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Input file not found. Please select a valid file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during transformation: {str(e)}")

    def update_selected_file_label(self, file_path):
        file_name = os.path.basename(file_path)
        self.selected_file_label.config(text=f"Selected File: {file_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVTransformerApp(root)
    root.mainloop()