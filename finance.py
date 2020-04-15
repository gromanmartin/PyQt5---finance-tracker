from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
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
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.createacc)
        # self.stack.setCurrentWidget(self.menu)

        self.menu.group_button.buttonClicked[int].connect(self.stack.setCurrentIndex)
        self.createacc.createacc_buttons.buttonClicked[int].connect(self.stack.setCurrentIndex)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


class MenuWindow(QWidget):

    def __init__(self):
        super(MenuWindow, self).__init__()
        self.setGeometry(0, 0, 350, 200)
        box = QVBoxLayout()

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
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
        self.setGeometry(0, 0, 350, 200)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        label = QLabel('Welcome to finance tracker')
        box = QVBoxLayout()
        box.addWidget(label)
        self.setLayout(box)
        self.show()


class CreateAccWindow(QWidget):

    def __init__(self):
        super(CreateAccWindow, self).__init__()
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        regex = QRegExp("[a-zA-Z1-9]+")
        validator = QRegExpValidator(regex)

        label = QLabel('Create a new account')
        label.setAlignment(Qt.AlignCenter)
        user_name_label = QLabel('Username')
        user_name_label.setFixedWidth(90)
        self.user_name_check = QLabel('')
        self.user_name_check.setFixedWidth(100)
        self.user_name_edit = QLineEdit()
        self.user_name_edit.setValidator(validator)
        self.user_name_edit.setFixedWidth(100)

        password_label = QLabel('Password')
        password_label.setFixedWidth(90)
        self.password_check = QLabel('')
        self.password_check.setFixedWidth(100)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setReadOnly(True)
        self.password_edit.setValidator(validator)
        self.password_edit.setFixedWidth(100)

        confirmpassword_label = QLabel('Confirm password')
        confirmpassword_label.setFixedWidth(90)
        self.confirmpassword_check = QLabel('')
        self.confirmpassword_check.setFixedWidth(100)
        self.confirmpassword_edit = QLineEdit()
        self.confirmpassword_edit.setEchoMode(QLineEdit.Password)
        self.confirmpassword_edit.setReadOnly(True)
        self.confirmpassword_edit.setValidator(validator)
        self.confirmpassword_edit.setFixedWidth(100)

        self.notpassword_label = QLabel('')
        self.notpassword_label.setFixedWidth(150)

        main_grid = QVBoxLayout()
        main_grid.addWidget(label)
        grids = []
        for i in range(0, 3):
            new_grid = QHBoxLayout()
            grids.append(new_grid)
            main_grid.addLayout(grids[i])

        form_list = [(user_name_label, self.user_name_edit, self.user_name_check),
                     (password_label, self.password_edit, self.password_check),
                     (confirmpassword_label, self.confirmpassword_edit, self.confirmpassword_check)]
        for i, pair in enumerate(form_list):
            grids[i].addWidget(pair[0])
            grids[i].addWidget(pair[1])
            grids[i].addWidget(pair[2])

        main_grid.addWidget(self.notpassword_label, alignment=Qt.AlignHCenter)
        self.user_name_edit.textEdited.connect(self.input_checking)
        self.password_edit.textEdited.connect(self.input_checking)
        self.confirmpassword_edit.textEdited.connect(self.input_checking)


        buttons_layout = QHBoxLayout()
        main_grid.addLayout(buttons_layout)
        buttons_layout.addStretch(50)

        self.create_button = QPushButton('Create account')
        self.create_button.setEnabled(False)
        back_button = QPushButton('Back')
        self.createacc_buttons = QButtonGroup()

        for i, button in enumerate([self.create_button, back_button]):
            button.setFixedWidth(100)
            buttons_layout.addWidget(button, alignment=Qt.AlignCenter)
            self.createacc_buttons.addButton(button)

        buttons_layout.addStretch(50)

        self.create_button.clicked.connect(self.create_user)

        self.createacc_buttons.setId(self.create_button, 4)  # ID = 4
        self.createacc_buttons.setId(back_button, 0)    # ID = 0 will move me back to main menu

        self.setLayout(main_grid)
        self.setGeometry(0, 0, 350, 200)
        self.show()

    def input_checking(self):
        un = str(self.user_name_edit.text())
        pw = str(self.password_edit.text())
        cpw = str(self.confirmpassword_edit.text())
        if len(un) > 4:
            self.password_edit.setReadOnly(False)
            self.confirmpassword_edit.setReadOnly(False)
            self.user_name_check.setText('')
            if any(i.isdigit() for i in pw) & any(i.isalpha() for i in pw):
                if len(pw) > 4:
                    if pw == cpw:
                        self.notpassword_label.setText('The passwords match')
                        self.notpassword_label.setStyleSheet('color: green')
                        self.password_check.setText('')
                        self.create_button.setEnabled(True)
                    else:
                        self.notpassword_label.setText('The passwords do not match')
                        self.notpassword_label.setStyleSheet('color: red')
                        self.password_check.setText('')
                        self.create_button.setEnabled(False)
                else:
                    self.notpassword_label.setText('')
                    self.password_check.setText('Min length is 5 chars')
                    self.password_check.setStyleSheet('color:red')
                    self.create_button.setEnabled(False)
            else:
                self.notpassword_label.setText('')
                self.password_check.setText('Min. 1 char, 1 num')
                self.password_check.setStyleSheet('color:red')
                self.create_button.setEnabled(False)
        else:
            self.user_name_check.setText('Min. length is 5 chars')
            self.user_name_check.setStyleSheet('color:red')
            self.notpassword_label.setText('')
            self.password_edit.setReadOnly(True)
            self.confirmpassword_edit.setReadOnly(True)
            self.create_button.setEnabled(False)

    def create_user(self):
        c = conn.cursor()
        user_name_text = self.user_name_edit.text()
        password_text = self.password_edit.text()
        try:
            c.execute(" INSERT INTO users VALUES (:user_name, :password)", {'user_name': user_name_text, 'password': password_text})
            conn.commit()
        except sqlite3.OperationalError:
            print('lol')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    conn = sqlite3.connect('database.db')
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
