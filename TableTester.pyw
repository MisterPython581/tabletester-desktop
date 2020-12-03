"""
    This file is part of TableTester Desktop.

    TableTester Desktop is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    TableTester Desktop is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TableTester Desktop.
    If not, see <https://www.gnu.org/licenses/>.
"""
import random
import sys

try:
    from PyQt5 import uic, QtWidgets # UI Module
except ImportError:
    print("Oops...\nAn error has occurred. We couldn't import the module \"PyQt5\" \
due to an ImportError raised by the Python interpreter. Please install it with the command: \
\n$pip install PyQt5")
    sys.exit(1)

home = "main.ui"
quiz = "quiz.ui"

# Load the two UI files
Ui_Home, QtBaseClass = uic.loadUiType(home)
Ui_Quiz, QtBaseClass = uic.loadUiType(quiz)


class Home(QtWidgets.QDialog, Ui_Home):
    """
        Home window of TableTester Desktop.
        It will display once you have opened it.
    """
    def __init__(self):
        super(Home, self).__init__()
        self.setupUi(self)
        with open("average.dat") as file:
            self.ui_average.setText(str(file.read().replace(".", ",")))  # Replace the character "." to ","
        self.ButtonRun.clicked.connect(run_quiz)
        self.reset.clicked.connect(reset)
        self.scoretemp = ""
        self.sntemp = ""


class Quiz(QtWidgets.QDialog, Ui_Quiz):
    def __init__(self):
        super(Quiz, self).__init__()
        self.setupUi(self)
        self.score = 0
        self.sn = 1
        self.s1 = random.randint(1, 10)
        self.s2 = random.randint(1, 10)
        self.home_redirect = False
        self.setWindowTitle("TableTester - Question %s/10" % self.sn)
        self.AskLabel.setText(" %s X %s" % (self.s1, self.s2))
        self.Next.clicked.connect(self.valid)
        self.Back.clicked.connect(self.exit)

    def valid(self):
        if int(self.Number.text()) == self.s1 * self.s2:
            self.score = self.score + 1
        self.sn = self.sn + 1
        if self.home_redirect:
            quizw.close()
            homew.show()
            self.score = 0
            self.sn = 1
            self.s1 = random.randint(1, 10)
            self.s2 = random.randint(1, 10)
            self.home_redirect = False
            self.setWindowTitle(f"TableTester - Question {self.sn}/10")
            self.AskLabel.setText(f" {self.s1} X {self.s2}")
            self.ResultLabel.setText("")
        if self.sn == 11:
            self.AskLabel.setText(f" {self.score} / 10")
            self.ResultLabel.setText(f"Vous avez correctement répondu à {self.score} des questions sur 10.")
            self.home_redirect = True
            change_average(self.score)
        else:
            self.setWindowTitle(f"TableTester - Question {self.sn}/10")
            self.s1 = random.randint(1, 10)
            self.s2 = random.randint(1, 10)
            self.AskLabel.setText(" %s X %s" % (self.s1, self.s2))
        self.scoretemp = str(self.score)
        self.sntemp = str(self.sn - 1)
        self.score_ui.setText("Score actuel : %s/%s" % (self.scoretemp, self.sntemp))

    def exit(self):
        quizw.close()
        homew.show()
        self.score = 0
        self.sn = 1
        self.s1 = random.randint(1, 10)
        self.s2 = random.randint(1, 10)
        self.home_redirect = False
        self.setWindowTitle("TableTester Desktop - Question %s/10" % self.sn)
        self.AskLabel.setText(" %s X %s" % (self.s1, self.s2))
        self.AskLabel.setText(" %s X %s" % (self.s1, self.s2))
        self.ResultLabel.setText("")


def change_average(value):
    file = open("average.dat", "r")
    average = file.read()
    file.close()
    average = str(average)
    average = float((float(average) + value) / 2)
    file = open("average.dat", "w")
    average = str(average)
    average = average[:4]
    file.write(average)
    file.close()
    homew.ui_average.setText(str(average))


def run_quiz():
    homew.close()
    quizw.show()


def reset():
    with open("average.dat", "w") as file:
        file.write("5.0")
    homew.ui_average.setText("5,00")


if __name__ == "__main__":
    # Create app object
    app = QtWidgets.QApplication(sys.argv)
    # Create windows
    quizw = Quiz()
    homew = Home()
    # Show window homew
    homew.show()
    # Wait to exit Python if there is a exec_() signal
    sys.exit(app.exec_())
