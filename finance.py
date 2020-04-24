from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
import pyqtgraph as pg
import sys
import numpy as np


class ApplicationWindow(QWidget):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.menu = MenuWindow()    # COMMENT FOR TEST
        self.login = LoginWindow()    # COMMENT FOR TEST
        self.createacc = CreateAccWindow()     # COMMENT FOR TEST
        self.core = CoreMenuWindow()

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Finance tracker')

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.stack.addWidget(self.menu)    # COMMENT FOR TEST
        self.stack.addWidget(self.login)  # COMMENT FOR TEST
        self.stack.addWidget(self.createacc)  # COMMENT FOR TEST
        self.stack.addWidget(self.core)
        self.corestack = QStackedWidget()
        # self.stack.addWidget(self.corestack)  # TESTING
        self.corestack.addWidget(self.core)
        # self.stack.setCurrentWidget(self.corestack)  # TESTING

        self.menu.group_button.buttonClicked[int].connect(self.stack.setCurrentIndex)             # COMMENT FOR TEST
        self.createacc.createacc_buttons.buttonClicked[int].connect(self.stack.setCurrentIndex)   # COMMENT FOR TEST
        self.createacc.resp_button_group.buttonClicked[int].connect(self.stack.setCurrentIndex)   # COMMENT FOR TEST
        self.createacc.resp_button_group.buttonClicked[int].connect(self.createacc.resp.close)    # COMMENT FOR TEST
        self.login.login_buttons.buttonClicked[int].connect(self.stack.setCurrentIndex)           # COMMENT FOR TEST
        self.login.resp_button_group.buttonClicked[int].connect(self.logged_in)                   # COMMENT FOR TEST
        # self.login.resp_button.clicked.connect(self.logged_in)
        self.login.resp_button_group.buttonClicked[int].connect(self.login.resp.close)            # COMMENT FOR TEST

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def logged_in(self):
        c = conn.cursor()
        self.stack.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.stack.addWidget(self.corestack)
        self.stack.setCurrentWidget(self.corestack)
        logged_username = self.login.login_auth()
        self.core.logged_label.setText('Logged in as: {}'.format(logged_username))
        self.stack.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        query = c.execute(" SELECT id FROM users WHERE username == '{}'".format(logged_username))
        self.core.logged_id = [a for a in query.fetchone()][0]
        self.core.general_setup()
        print(self.core.logged_id)


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
        regex = QRegExp("[a-zA-Z1-9]+")
        validator = QRegExpValidator(regex)

        label = QLabel('Login')
        label.setAlignment(Qt.AlignCenter)

        user_name_label = QLabel('Username')
        user_name_label.setFixedWidth(50)
        self.user_name_edit = QLineEdit()
        self.user_name_edit.setValidator(validator)
        self.user_name_edit.setFixedWidth(150)
        password_label = QLabel('Password')
        password_label.setFixedWidth(50)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setValidator(validator)
        self.password_edit.setFixedWidth(150)

        self.wrong_label = QLabel('')
        self.wrong_label.setFixedWidth(150)

        main_grid = QVBoxLayout()
        main_grid.addWidget(label)
        grids = []
        for i in range(0, 2):
            new_grid = QHBoxLayout()
            grids.append(new_grid)
            main_grid.addLayout(grids[i])

        form_list = [(user_name_label, self.user_name_edit),
                     (password_label, self.password_edit)]
        for i, pair in enumerate(form_list):
            grids[i].addWidget(pair[0])
            grids[i].addWidget(pair[1])
        main_grid.addWidget(self.wrong_label, alignment=Qt.AlignHCenter)

        buttons_layout = QHBoxLayout()
        main_grid.addLayout(buttons_layout)
        buttons_layout.addStretch(50)

        self.login_button = QPushButton('Login')
        self.login_button.setEnabled(False)
        self.back_button = QPushButton('Back')
        self.login_buttons = QButtonGroup()

        for i, button in enumerate([self.login_button, self.back_button]):
            button.setFixedWidth(100)
            buttons_layout.addWidget(button, alignment=Qt.AlignCenter)
            self.login_buttons.addButton(button)

        self.login_buttons.setId(self.back_button, 0)
        buttons_layout.addStretch(50)

        self.resp = QDialog()
        self.resp.resize(200, 100)
        self.resp.setWindowTitle(' ')
        self.resp.setWindowModality(Qt.ApplicationModal)
        self.resp_layout = QVBoxLayout()
        self.resp_label = QLabel('Login Successful!', self.resp)
        self.resp_label.setAlignment(Qt.AlignCenter)
        self.resp_button = QPushButton('Ok', self.resp)
        self.resp_button_group = QButtonGroup()
        self.resp_layout.addWidget(self.resp_label)
        self.resp_layout.addWidget(self.resp_button)
        self.resp.setLayout(self.resp_layout)

        self.login_button.clicked.connect(self.login_clicked)
        self.user_name_edit.textEdited.connect(self.login_auth)
        self.password_edit.textEdited.connect(self.login_auth)

        self.setLayout(main_grid)
        self.show()

    def login_auth(self):
        un = self.user_name_edit.text()
        pw = self.password_edit.text()
        c = conn.cursor()
        c.execute(" SELECT username FROM users")
        conn.commit()
        users_list = [u[0] for u in c.fetchall()]
        c.execute(" SELECT password FROM users")
        conn.commit()
        pws_list = [u[0] for u in c.fetchall()]
        if un in users_list:
            self.wrong_label.setText('')
            un_id = users_list.index(un)
            if pw == pws_list[un_id]:
                self.login_button.setEnabled(True)
            else:
                self.login_button.setEnabled(False)
        else:
            self.login_button.setEnabled(False)
            self.wrong_label.setText('The username does not exist')
            self.wrong_label.setStyleSheet('color:red')
        return un

    def login_clicked(self):
        self.resp_button_group.addButton(self.resp_button, 3)
        self.resp.exec_()


class CreateAccWindow(QWidget):

    def __init__(self):
        super(CreateAccWindow, self).__init__()
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
        self.back_button = QPushButton('Back')
        self.createacc_buttons = QButtonGroup()

        for i, button in enumerate([self.create_button, self.back_button]):
            button.setFixedWidth(100)
            buttons_layout.addWidget(button, alignment=Qt.AlignCenter)
            self.createacc_buttons.addButton(button)

        buttons_layout.addStretch(50)

        self.create_button.clicked.connect(self.create_user)
        self.createacc_buttons.setId(self.create_button, 4)  # ID = 4
        self.createacc_buttons.setId(self.back_button, 0)    # ID = 0 will move me back to main menu

        self.resp = QDialog()
        self.resp.resize(200, 100)
        self.resp.setWindowTitle(' ')
        self.resp.setWindowModality(Qt.ApplicationModal)
        self.resp_account_exist = True
        self.resp_layout = QVBoxLayout()
        self.resp_label = QLabel('Your account has been created. \n Click Ok to return to main menu.', self.resp)
        self.resp_label.setAlignment(Qt.AlignCenter)
        self.resp_button = QPushButton('Ok', self.resp)
        self.resp_button_group = QButtonGroup()
        self.resp_button_group_id = 0
        self.resp_layout.addWidget(self.resp_label)
        self.resp_layout.addWidget(self.resp_button)
        self.resp.setLayout(self.resp_layout)

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
        c.execute(" SELECT username FROM users")
        db_user_names = [un[0] for un in c.fetchall()]
        if user_name_text not in db_user_names:
            self.resp_button_group_id = 0
            self.resp_button_group.addButton(self.resp_button, self.resp_button_group_id)
            self.resp_label.setText('Your account has been created. \n Click Ok to return to main menu.')
            c.execute(" SELECT COUNT(id) FROM users")
            user_id = c.fetchone()[0]
            try:
                c.execute(" INSERT INTO users VALUES (:id, :user_name, :password)",
                          {'id': user_id, 'user_name': user_name_text, 'password': password_text})
                conn.commit()
                self.resp.exec_()
            except sqlite3.OperationalError:
                self.resp_label.setText('Something went wrong')
                self.resp.exec_()
        else:
            self.resp_button_group_id = 4
            self.resp_button_group.addButton(self.resp_button, self.resp_button_group_id)
            self.resp_label.setText('Choose different username')
            self.resp.exec_()


class CoreMenuWindow(QWidget):

    def __init__(self):
        super(CoreMenuWindow, self).__init__()
        self.setGeometry(0, 0, 750, 550)
        box = QVBoxLayout()
        self.plot_window = PlotWindow()
        self.plot_window.hide()
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        topbar = QHBoxLayout()
        self.current_widget_label = QLabel('Overview')
        self.current_widget_label.setAlignment(Qt.AlignVCenter)
        self.current_widget_label.setFixedSize(700, 100)
        self.current_widget_label.setStyleSheet('font: 42pt')

        self.logged_id = 0

        self.logged_label = QLabel()
        self.logged_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setLineWidth(1)
        topbar.addStretch(100)
        topbar.addWidget(self.current_widget_label)
        topbar.addWidget(self.logged_label)
        topbar.addStretch(100)

        self.leftmenu_overview_button = QPushButton('Overview')
        self.leftmenu_history_button = QPushButton('History')
        self.leftmenu_charts_button = QPushButton('Charts')
        self.leftmenu_manage_button = QPushButton('Manage')
        self.leftmenu_exit_button = QPushButton('Exit')

        self.leftmenu_button_group = QButtonGroup()
        leftmenu_layout = QVBoxLayout()
        for i, button in enumerate([self.leftmenu_overview_button, self.leftmenu_history_button,
                                    self.leftmenu_charts_button, self.leftmenu_manage_button, self.leftmenu_exit_button]):
            button.setFixedSize(150, 50)
            button.setStyleSheet('border:1px solid black')
            self.leftmenu_button_group.addButton(button)
            self.leftmenu_button_group.setId(button, i+1)
            leftmenu_layout.addWidget(button, alignment=Qt.AlignLeft)

        self.all_frames = []

        self.overview_frame = QFrame()
        self.all_frames.append(self.overview_frame)
        self.overview_layout = QVBoxLayout()
        self.overview_frame.setLayout(self.overview_layout)
        self.accbalance_label = QLabel()
        self.table_overview = QTableWidget()

        self.history_frame = QFrame()
        self.all_frames.append(self.history_frame)
        self.history_layout = QVBoxLayout()
        self.history_frame.setLayout(self.history_layout)
        self.table_history = QTableWidget()

        self.manage_frame = QFrame()
        self.all_frames.append(self.manage_frame)
        self.manage_layout = QVBoxLayout()
        self.manage_frame.setLayout(self.manage_layout)

        self.charts_frame = QFrame()
        self.charts_layout = QVBoxLayout()
        self.charts_frame.setLayout(self.charts_layout)
        self.all_frames.append(self.charts_frame)
        self.plot_buttons = QButtonGroup()

        self.mainwindow_layout = QHBoxLayout()
        box.addLayout(topbar)
        box.addWidget(separator)
        box.addLayout(self.mainwindow_layout)
        self.mainwindow_layout.addLayout(leftmenu_layout)
        self.mainwindow_layout.addWidget(self.overview_frame)
        self.mainwindow_layout.addWidget(self.history_frame)
        self.mainwindow_layout.addWidget(self.charts_frame)
        self.mainwindow_layout.addWidget(self.manage_frame)

        self.leftmenu_overview_button.clicked.connect(self.select_overview)
        self.leftmenu_history_button.clicked.connect(self.select_history)
        self.leftmenu_charts_button.clicked.connect(self.select_charts)
        self.leftmenu_manage_button.clicked.connect(self.select_manage)
        self.leftmenu_exit_button.clicked.connect(sys.exit)

        self.setLayout(box)
        self.show()

    def general_setup(self):    # This function serves as connection with user ID from login page
        self.setup_overview()
        self.setup_history()
        self.setup_manage()
        self.setup_charts()
        self.select_overview()

    def update_overview(self):
        c = conn.cursor()
        query = c.execute("""   SELECT SUM(amount)
                                        FROM finances
                                        WHERE id_user == {}              
                                    """.format(self.logged_id))
        bal = query.fetchone()
        self.accbalance_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.accbalance_label.setText('Balance: {}$'.format(bal[0]))
        if bal[0] > 0:
            self.accbalance_label.setStyleSheet('color: green')
        else:
            self.accbalance_label.setStyleSheet('color: red')

        query = c.execute("""   SELECT amount, type, category, date
                                    FROM finances
                                    WHERE id_user == {}
                                    ORDER BY date DESC
                                    LIMIT 5""".format(self.logged_id))
        querylist = [a for a in query.fetchall()]
        for i in range(0, len(querylist)):
            for j in range(0, 4):
                if j == 0:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.EditRole, querylist[i][j])
                    self.table_overview.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(querylist[i][j])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_overview.setItem(i, j, item)

    def setup_overview(self):
        c = conn.cursor()
        self.overview_frame.hide()

        query = c.execute("""   SELECT SUM(amount)
                                FROM finances
                                WHERE id_user == {}              
                            """.format(self.logged_id))
        bal = query.fetchone()
        self.accbalance_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.accbalance_label.setText('Balance: {}$'.format(bal[0]))
        if bal[0] > 0:
            self.accbalance_label.setStyleSheet('color: green')
        else:
            self.accbalance_label.setStyleSheet('color: red')

        table_label = QLabel('Table showing last 5 balance changes')
        table_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.table_overview.setMaximumHeight(250)
        self.table_overview.setRowCount(5)
        self.table_overview.setColumnCount(4)
        header = self.table_overview.horizontalHeader()
        for i in range(0, 4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        header2 = self.table_overview.verticalHeader()
        for i in range(0, 5):
            header2.setSectionResizeMode(i, QHeaderView.Stretch)

        self.table_overview.setHorizontalHeaderLabels(('Amount', 'In/Out', 'Category', 'Date'))
        query = c.execute("""   SELECT amount, type, category, date
                            FROM finances
                            WHERE id_user == {}
                            ORDER BY date DESC
                            LIMIT 5""".format(self.logged_id))
        querylist = [a for a in query.fetchall()]
        for i in range(0, len(querylist)):
            for j in range(0, 4):
                if j == 0:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.EditRole, querylist[i][j])
                    self.table_overview.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(querylist[i][j])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_overview.setItem(i, j, item)

        self.overview_layout.addWidget(self.accbalance_label)
        self.overview_layout.addWidget(table_label)
        self.overview_layout.addWidget(self.table_overview)

    def select_overview(self):
        for frame in self.all_frames:
            frame.hide()
        self.update_overview()
        self.overview_frame.show()
        self.current_widget_label.setText('Overview')

    def update_history(self):
        c = conn.cursor()
        query = c.execute("""   SELECT amount, type, category, date
                                                            FROM finances 
                                                            WHERE id_user == {}
                                                            """.format(self.logged_id))
        querylist = [a for a in query.fetchall()]
        self.table_history.setRowCount(len(querylist))
        for i in range(0, len(querylist)):
            for j in range(0, 4):
                if j == 0:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.EditRole, querylist[i][j])
                    self.table_history.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(querylist[i][j])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_history.setItem(i, j, item)

    def setup_history(self):
        c = conn.cursor()
        self.history_frame.hide()

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignTop)
        label = QLabel('Filters:')
        label.setAlignment(Qt.AlignVCenter)
        self.cb1 = QComboBox()
        self.cb2 = QComboBox()
        self.cb3 = QComboBox()
        self.cb4 = QComboBox()

        inout_list = ['In/Out', 'in', 'out']
        cat_list = ['Category', 'Income', 'Other income', 'Shopping', 'Rent', 'Fun', 'Other bills']
        year_list = ['Year', '2020', '2019', '2018']
        date_list = ['Month', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                     'October', 'November', 'December']
        lists = [inout_list, cat_list, year_list, date_list]
        self.cb1.addItems(inout_list)
        self.cb2.addItems(cat_list)
        self.cb3.addItems(year_list)
        self.cb4.addItems(date_list)

        # self.confirm_button = QPushButton('Confirm')

        top_layout.addWidget(label)
        top_layout.addWidget(self.cb1)
        top_layout.addWidget(self.cb2)
        top_layout.addWidget(self.cb3)
        top_layout.addWidget(self.cb4)
        # top_layout.addWidget(self.confirm_button)

        self.table_history.setMaximumHeight(250)
        self.table_history.setColumnCount(4)

        header = self.table_history.horizontalHeader()
        for i in range(0, 4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        self.table_history.setHorizontalHeaderLabels(('Amount', 'In/Out', 'Category', 'Date'))

        query = c.execute("""   SELECT amount, type, category, date
                                                    FROM finances 
                                                    WHERE id_user == {}
                                                    """.format(self.logged_id))
        querylist = [a for a in query.fetchall()]
        self.table_history.setRowCount(len(querylist))
        for i in range(0, len(querylist)):
            for j in range(0, 4):
                if j == 0:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.EditRole, querylist[i][j])
                    self.table_history.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(querylist[i][j])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_history.setItem(i, j, item)

        # self.confirm_button.clicked.connect(self.history_query)
        self.cb1.currentIndexChanged.connect(self.history_query)
        self.cb2.currentIndexChanged.connect(self.history_query)
        self.cb3.currentIndexChanged.connect(self.history_query)
        self.cb4.currentIndexChanged.connect(self.history_query)

        self.history_layout.addLayout(top_layout)
        self.history_layout.addWidget(self.table_history)

    def select_history(self):
        for frame in self.all_frames:
            frame.hide()
        self.update_history()
        self.history_frame.show()
        self.current_widget_label.setText('History')

    def history_query(self):
        c = conn.cursor()
        cblist = [self.cb1.currentIndex(), self.cb2.currentIndex(), self.cb3.currentIndex(), self.cb4.currentIndex()]
        c3_year = self.cb3.currentText()[:4]
        c4_month = self.cb4.currentText()
        dict= {'Month':'00', 'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07',
               'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}
        crits = []
        c1_text = "type =='{}'".format(self.cb1.currentText())
        c2_text = "category == '{}'".format(self.cb2.currentText())
        c3_text = "date LIKE '%{}%'".format(c3_year)
        c4_text = "date LIKE '%-{}-%'".format(dict[c4_month])
        texts = [c1_text, c2_text, c3_text, c4_text]
        for i, item in enumerate(cblist):
            if item > 0:
                crits.append(texts[i])
        where_string = 'AND ' + ' AND '.join(crits)
        # print(where_string)
        if where_string == '':
            query = c.execute("""   SELECT amount, type, category, date
                                            FROM finances 
                                            """)
            querylist = [a for a in query.fetchall()]
        else:
            query = c.execute("""   SELECT amount, type, category, date
                                            FROM finances 
                                            WHERE id_user == {}
                                            """.format(self.logged_id) + where_string)
            querylist = [a for a in query.fetchall()]
        self.table.setRowCount(len(querylist))
        for i in range(0, len(querylist)):
            for j in range(0, 4):
                if j == 0:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.EditRole, querylist[i][j])
                    self.table.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(querylist[i][j])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(i, j, item)

    def setup_manage(self):
        self.manage_frame.hide()

        main_label = QLabel('Insert a new income/expense:')
        main_label.setAlignment(Qt.AlignLeft)
        amount_label = QLabel('Amount')
        amount_label.setFixedWidth(100)
        self.amount_edit = QLineEdit()
        self.amount_edit.setFixedWidth(100)
        self.amount_edit.setValidator(QDoubleValidator(0.99, 99.99, 2))

        type_label = QLabel('Type')
        type_label.setFixedWidth(100)
        self.type_edit = QComboBox()
        self.type_edit.setFixedWidth(100)
        inout_list = ['In/Out', 'in', 'out']

        category_label = QLabel('Category')
        category_label.setFixedWidth(100)
        self.category_edit = QComboBox()
        self.category_edit.setEnabled(True)
        self.category_edit.setFixedWidth(100)
        self.type_edit.addItem('In/Out', ['Category'])
        self.type_edit.addItem('in', ['Category', 'Income', 'Other income'])
        self.type_edit.addItem('out',['Category', 'Shopping', 'Rent', 'Fun', 'Other bills'])

        date_label = QLabel('Date (YYYY-MM-DD)')
        date_label.setFixedWidth(100)
        self.date_edit = QLineEdit()
        date_regex = QRegExp("(19[0-9][0-9]|20[0-2][0-9])-(0[1-9]|[1][0-2])-(0[1-9]|[12][0-9]|3[01])")
        valid = QRegExpValidator(date_regex)
        self.date_edit.setValidator(valid)
        self.date_edit.setFixedWidth(100)

        self.insert_button = QPushButton('Insert')
        self.insert_button.setFixedWidth(100)
        self.insert_button.setEnabled(False)
        self.insert_label = QLabel('')
        self.insert_label.setStyleSheet('color:red')
        self.insert_label.setFixedWidth(150)
        insert_layout = QHBoxLayout()
        insert_layout.addWidget(self.insert_button, alignment=Qt.AlignLeft)
        insert_layout.addWidget(self.insert_label, alignment=Qt.AlignLeft)
        insert_layout.addStretch(100)

        main_grid = QVBoxLayout()
        main_grid.addWidget(main_label)
        grids = []
        for i in range(0, 4):
            new_grid = QHBoxLayout()
            grids.append(new_grid)
            main_grid.addLayout(grids[i])

        form_list = [(amount_label, self.amount_edit), (type_label, self.type_edit), (category_label, self.category_edit),
                     (date_label, self.date_edit)]
        for i, pair in enumerate(form_list):
            grids[i].addWidget(pair[0])
            grids[i].addWidget(pair[1])
            grids[i].addStretch(100)
        main_grid.addLayout(insert_layout)
        main_grid.addStretch(200)

        self.amount_edit.textEdited.connect(self.manage_insert_button_enable)
        self.type_edit.currentIndexChanged.connect(self.manage_insert_button_enable)

        self.type_edit.currentIndexChanged.connect(self.block_cat)
        self.block_cat(self.type_edit.currentIndex())

        self.category_edit.currentIndexChanged.connect(self.manage_insert_button_enable)
        self.date_edit.textEdited.connect(self.manage_insert_button_enable)
        self.insert_button.clicked.connect(self.insert_into_db)
        self.manage_layout.addLayout(main_grid)

    def select_manage(self):
        for frame in self.all_frames:
            frame.hide()
        self.manage_frame.show()
        self.current_widget_label.setText('Manage')

    def manage_insert_button_enable(self):

        if self.amount_edit.text() == '':
            am = 0
        else:
            am = float(self.amount_edit.text())
        type_ind = self.type_edit.currentIndex()
        cat_ind = self.category_edit.currentIndex()
        date_text = len(self.date_edit.text())

        if (am > 0) & (type_ind > 0) & (cat_ind > 0) & (date_text == 10):
            self.insert_button.setEnabled(True)
            self.insert_label.setText('')
        else:
            self.insert_button.setEnabled(False)
            self.insert_label.setText('Fill out all the fields to continue')

    def block_cat(self, index):
        self.category_edit.clear()
        data = self.type_edit.itemData(index)
        if data is not None:
            self.category_edit.addItems(data)

    def insert_into_db(self):
        c = conn.cursor()
        amount = float(self.amount_edit.text())
        type = self.type_edit.currentText()
        if type == 'out':
            amount = - amount
        cat = self.category_edit.currentText()
        date = self.date_edit.text()
        print(amount, type, cat, date)
        query = c.execute(" SELECT id FROM finances")
        last_id = [a[0] for a in query.fetchall()][-1]
        new_id = last_id + 1
        id_u = self.logged_id
        c.execute(""" INSERT INTO finances 
                              VALUES (:id, :amount, :type, :category, :date, :id_user) """, {'id': new_id, 'amount': amount,
                                'type': type, 'category': cat, 'date': date, 'id_user': id_u})
        conn.commit()
        success_dia = QDialog()
        success_dia.resize(200, 100)
        success_dia.setWindowTitle(' ')
        success_dia.setWindowModality(Qt.ApplicationModal)
        success_dia_layout = QVBoxLayout()
        success_dia_label = QLabel('Success!', success_dia)
        success_dia_label.setAlignment(Qt.AlignCenter)
        success_dia_button = QPushButton('Ok', success_dia)
        success_dia_button_group = QButtonGroup()
        success_dia_layout.addWidget(success_dia_label)
        success_dia_layout.addWidget(success_dia_button)
        success_dia_button.clicked.connect(success_dia.close)
        success_dia.setLayout(success_dia_layout)
        success_dia.exec_()

    def setup_charts(self):
        self.charts_frame.hide()

        top_label = QLabel('Choose a graph to plot')

        plot1_label = QLabel('Income')
        plot1_label.setFixedWidth(100)
        plot1_cb = QComboBox()
        plot1_cb.setFixedWidth(100)
        plot1_cb_list = ['Pick one', 'By month', 'By category']
        plot1_cb.addItems(plot1_cb_list)
        plot1_button = QPushButton('Plot1')

        plot2_label = QLabel('Expense')
        plot2_label.setFixedWidth(100)
        plot2_cb = QComboBox()
        plot2_cb.setFixedWidth(100)
        plot2_cb_list = ['Pick one', 'By month', 'By category']
        plot2_cb.addItems(plot2_cb_list)
        plot2_button = QPushButton('Plot2')

        plot3_label = QLabel('In vs out')
        plot3_label.setFixedWidth(100)
        self.plot3_cb = QComboBox()
        self.plot3_cb.setFixedWidth(100)
        plot3_cb_list = ['Pick one', 'Total', 'By category', 'By month']
        self.plot3_cb.addItems(plot3_cb_list)
        plot3_button = QPushButton('Plot')

        main_grid = QVBoxLayout()
        main_grid.addWidget(top_label)
        grids = []
        for i in range(0, 3):
            new_grid = QHBoxLayout()
            grids.append(new_grid)
            main_grid.addLayout(grids[i])

        form_list = [(plot1_label, plot1_cb, plot1_button), (plot2_label, plot2_cb, plot2_button),
                     (plot3_label, self.plot3_cb, plot3_button)]
        for i, pair in enumerate(form_list):
            grids[i].addWidget(pair[0])
            grids[i].addWidget(pair[1])
            grids[i].addWidget(pair[2])
            grids[i].addStretch(100)
        main_grid.addStretch(200)
        for i, button in enumerate([plot1_button, plot2_button, plot3_button]):
            self.plot_buttons.addButton(button, i+1)

        # self.plot3_cb.currentIndexChanged.connect(self.set_plot_data)
        plot3_button.clicked.connect(self.set_plot_data)

        self.charts_layout.addLayout(main_grid)

    def select_charts(self):
        for frame in self.all_frames:
            frame.hide()
        self.charts_frame.show()
        self.current_widget_label.setText('Charts')

    def get_plot_data(self):
        c = conn.cursor()
        which = self.plot3_cb.currentIndex()
        print(which)
        if which == 1:
            query = c.execute("""   SELECT SUM(amount), type
                                        FROM finances
                                        WHERE id_user == {}
                                        GROUP BY(type)
                                                """.format(self.logged_id))
            res = [a for a in query.fetchall()]

        elif which == 2:
            query = c.execute("""   SELECT amount
                            FROM finances
                            WHERE id_user == {}
                            GROUP BY(category)
                                    """.format(self.logged_id))
            res = [a for a in query.fetchall()]
        elif which == 3:
            query = c.execute("""   SELECT SUM(amount),
                                    CASE
                                                WHEN date LIKE '%-01-%' THEN 'January'
                                                WHEN date LIKE '%-02-%' THEN 'February'
                                                WHEN date LIKE '%-03-%' THEN 'March'
                                                WHEN date LIKE '%-04-%' THEN 'April'
                                                WHEN date LIKE '%-05-%' THEN 'May'
                                                WHEN date LIKE '%-06-%' THEN 'June'
                                                WHEN date LIKE '%-07-%' THEN 'July'
                                                WHEN date LIKE '%-08-%' THEN 'August'
                                                WHEN date LIKE '%-09-%' THEN 'September'
                                                WHEN date LIKE '%-10-%' THEN 'October'
                                                WHEN date LIKE '%-11-%' THEN 'November'
                                                WHEN date LIKE '%-12-%' THEN 'December'
                                    END AS dateText
                                    FROM finances
                                    WHERE id_user == {}
                                    GROUP BY dateText
                                                """.format(self.logged_id))
            res = [a for a in query.fetchall()]
        else:
            res = [(0, 'ERROR')]
        return res

    def set_plot_data(self):
        data = self.get_plot_data()
        win = pg.plot(title='Simple Bar Chart')
        y = np.asarray([a[0] for a in data])
        y[]
        x = np.asarray([a[1] for a in data])
        # y = np.linspace(0, 2, num=2)
        x = np.arange(2)
        # y1 = np.linspace(0, 20, num=20)
        # x = np.arange(20)
        bg1 = pg.BarGraphItem(x=x, height=y, width=0.6, brush='b')
        win.addItem(bg1)
        win.setTitle('Simple Bar Chart: Car Distribution')
        # win.setLabel('left', "Frequency", )
        # win.setLabel('bottom', "Number of Gears")


class PlotWindow(QWidget):

    def __init__(self):
        super(PlotWindow, self).__init__()
        plot_layout = QVBoxLayout()
        # self.graph = pg.plot()
        # hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        # self.graph.plot(hour, temperature)
        # plot_layout.addWidget(self.graph)
        self.setLayout(plot_layout)

    def plot(self, data):

        y = [a[0] for a in data]
        print(y)
        x = [a[1] for a in data]
        print(x)
        bg = pg.BarGraphItem(x=x, height=y, width=1)
        self.graph.addItem(bg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    conn = sqlite3.connect('database.db')
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
