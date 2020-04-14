from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class ApplicationWindow(QWidget):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.menu = MenuWindow()
        self.login = LoginWindow()
        self.createacc = CreateAccWindow()

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Finance tracker')

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.green)
        self.setPalette(p)

        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.createacc)
        self.stack.setCurrentWidget(self.menu)

        self.menu.group_button.buttonClicked[int].connect(self.stack.setCurrentIndex)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


class MenuWindow(QWidget):

    def __init__(self):
        super(MenuWindow, self).__init__()
        self.setGeometry(0, 0, 250, 200)
        box = QVBoxLayout()

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.red)
        self.setPalette(p)

        label = QLabel('Welcome to finance tracker')
        label.setStyleSheet('font: 24pt')
        box.addWidget(label, alignment=Qt.AlignCenter)

        login_button = QPushButton('Login')
        new_button = QPushButton('Create a new account')
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(qApp.exit)

        self.group_button = QButtonGroup()
        for i, button in enumerate([login_button, new_button, exit_button]):
            button.setStyleSheet('font: 14pt')
            button.setFixedSize(200, 50)
            box.addWidget(button, alignment=Qt.AlignCenter)
            self.group_button.addButton(button)
            self.group_button.setId(button, i+1)

        self.setLayout(box)
        self.show()


class LoginWindow(QWidget):

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setGeometry(0, 0, 250, 200)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)

        label = QLabel('Welcome to finance tracker')
        box = QVBoxLayout()
        box.addWidget(label)
        self.setLayout(box)
        self.show()


class CreateAccWindow(QWidget):

    def __init__(self):
        super(CreateAccWindow, self).__init__()
        self.setGeometry(0, 0, 250, 200)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.yellow)
        self.setPalette(p)

        label = QLabel('Welcome to finance tracker')
        box = QVBoxLayout()
        box.addWidget(label)
        self.setLayout(box)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
