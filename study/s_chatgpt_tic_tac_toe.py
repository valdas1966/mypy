import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.buttons = [[QPushButton('') for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].clicked.connect(lambda: self.play(row, col))
                grid.addWidget(self.buttons[row][col], row, col)

        self.player = 'X'

        self.show()

    def play(self, row, col):
        button = self.sender()
        if button.text() != '':
            print('That spot is already taken!')
            return
        button.setText(self.player)
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
        self.check_game_over()

    def check_game_over(self):
        # check rows
        for row in range(3):
            if self.buttons[row][0].text() != '' and self.buttons[row][0].text() == self.buttons[row][1].text() == self.buttons[row][2].text():
                self.game_over()
                return

        # check columns
        for col in range(3):
            if self.buttons[0][col].text() != '' and self.buttons[0][col].text() == self.buttons[1][col].text() == self.buttons[2][col].text():
                self.game_over()
                return

        # check diagonals
        if self.buttons[0][0].text() != '' and self.buttons[0][0].text() == self.buttons[1][1].text() == self.buttons[2][2].text():
            self.game_over()
            return
        if self.buttons[0][2].text() != '' and self.buttons[0][2].text() == self.buttons[1][1].text() == self.buttons[2][0].text():
            self.game_over()
            return

        # check for a draw
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col].text() == '':
                    return

        self.game_over()

    def game_over(self):
        print('Game over!')
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].setEnabled(False)

app = QApplication(sys.argv)
game = TicTacToe()
sys.exit(app.exec_())
