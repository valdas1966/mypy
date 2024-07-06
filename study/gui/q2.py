import tkinter as tk
from tkinter import messagebox

class QuestionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Question")

        # Maximize the window
        self.root.state('zoomed')  # This works on Windows and macOS

        # Configure the grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.question_label = tk.Label(root, text="What is the capital of France?", font=("Helvetica", 24))
        self.question_label.grid(row=0, column=0, pady=20)

        self.answer_entry = tk.Entry(root, font=("Helvetica", 20), width=30)
        self.answer_entry.grid(row=1, column=0, pady=10)
        self.answer_entry.focus_set()  # Set cursor focus to the text box

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer, font=("Helvetica", 20))
        self.submit_button.grid(row=2, column=0, pady=10)

        # Bind the Enter key to the submit button
        self.root.bind('<Return>', lambda event: self.submit_button.invoke())

    def submit_answer(self):
        answer = self.answer_entry.get()
        if answer.lower() == "paris":
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showinfo("Result", "Incorrect. The correct answer is Paris.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = QuestionGUI(root)
    root.mainloop()
