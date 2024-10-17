import tkinter as tk
from tkinter import filedialog

# Function to open a file browser and select a textbook excerpt (PDF or DOCX)
def open_textbook_browser():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a Textbook Excerpt", 
        filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")]
    )
    return file_path

# Function to open a file browser and select note slides (PPT or PPTX)
def open_notes_browser():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Note Slides", 
        filetypes=[("PowerPoint files", "*.ppt *.pptx")]
    )
    return file_path

# Main function to browse, read, and return file paths for the textbook and note slides
def browse_files():
    textbook_path = open_textbook_browser()  # Open the file browser for textbook excerpt
    notes_path = open_notes_browser()  # Open the file browser for note slides

    return textbook_path, notes_path  # Return the paths to both files for further use

# Example of how to use the function
# textbook, notes = browse_files()
# print("Textbook Path:", textbook)
# print("Notes Path:", notes)
