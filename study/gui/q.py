import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class QuestionGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Question")

        layout = QGridLayout()

        self.question_label = QLabel("What is the capital of France?")
        self.question_label.setFont(QFont("Heebo", 36, QFont.Bold))
        layout.addWidget(self.question_label, 0, 0, 1, 2, alignment=Qt.AlignCenter)

        self.answer_entry = QLineEdit(self)
        self.answer_entry.setFont(QFont("Heebo", 32, QFont.Bold))
        self.answer_entry.setStyleSheet(
            "border: 2px solid black; "
            "padding: 20px; "
            "margin-top: 70px;"
        )
        layout.addWidget(self.answer_entry, 1, 0, 1, 2, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Set cursor focus to the text box
        self.answer_entry.setFocus()

        # Connect the Enter key to the submit_answer method
        self.answer_entry.returnPressed.connect(self.submit_answer)

    def submit_answer(self):
        answer = self.answer_entry.text()
        if answer.lower() == "paris":
            QMessageBox.information(self, "Result", "Correct!")
        else:
            QMessageBox.information(self, "Result", "Incorrect. The correct answer is Paris.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = QuestionGUI()
    gui.showMaximized()
    sys.exit(app.exec_())
