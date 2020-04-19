from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
# from createacc_module import CreateAccWindow
import sys


class ApplicationWindow(QWidget):

    def __init__(self):
        super(ApplicationWindow, self).__init__()
        # self.menu = MenuWindow()
        # self.login = LoginWindow()
        # self.createacc = CreateAccWindow()
        self.core = CoreMenuWindow()

        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle('Finance tracker')

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)



        # self.stack.addWidget(self.menu)
        # self.stack.addWidget(self.login)
        # self.stack.addWidget(self.createacc)
        self.stack.addWidget(self.core)
        self.corestack = QStackedWidget()
        self.stack.addWidget(self.corestack)  # TESTING
        self.corestack.addWidget(self.core)
        self.stack.setCurrentWidget(self.corestack)  # TESTING

        # self.menu.group_button.buttonClicked[int].connect(self.stack.setCurrentIndex)
        # self.createacc.createacc_buttons.buttonClicked[int].connect(self.stack.setCurrentIndex)
        # self.createacc.resp_button_group.buttonClicked[int].connect(self.stack.setCurrentIndex)
        # self.createacc.resp_button_group.buttonClicked[int].connect(self.createacc.resp.close)
        # self.login.login_buttons.buttonClicked[int].connect(self.stack.setCurrentIndex)
        # self.login.resp_button_group.buttonClicked[int].connect(self.logged_in) # TO BE CONTINUED
        # # self.login.resp_button.clicked.connect(self.logged_in)
        # self.login.resp_button_group.buttonClicked[int].connect(self.login.resp.close)


        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def logged_in(self):
        self.stack.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.stack.addWidget(self.corestack)
        self.stack.setCurrentWidget(self.corestack)
        logged_username = self.login.login_auth()
        self.core.logged_label.setText('Logged in as: {}'.format(logged_username))
        self.stack.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)


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

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        topbar = QHBoxLayout()
        self.current_widget_label = QLabel('Overview')
        self.current_widget_label.setAlignment(Qt.AlignVCenter)
        self.current_widget_label.setFixedSize(700, 100)
        self.current_widget_label.setStyleSheet('font: 42pt')

        self.logged_username = ''
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
        self.leftmenu_tbc_button = QPushButton('Manage')
        self.leftmenu_exit_button = QPushButton('Logout')

        self.leftmenu_button_group = QButtonGroup()
        leftmenu_layout = QVBoxLayout()
        for i, button in enumerate([self.leftmenu_overview_button, self.leftmenu_history_button,
                                    self.leftmenu_charts_button, self.leftmenu_tbc_button, self.leftmenu_exit_button]):
            button.setFixedSize(150, 50)
            button.setStyleSheet('border:1px solid black')
            self.leftmenu_button_group.addButton(button)
            self.leftmenu_button_group.setId(button, i+1)
            leftmenu_layout.addWidget(button, alignment=Qt.AlignLeft)

        self.all_frames = []

        self.overview_frame = QFrame()
        self.setup_overview()
        self.history_frame = QFrame()
        self.setup_history()

        self.mainwindow_layout = QHBoxLayout()
        box.addLayout(topbar)
        box.addWidget(separator)
        box.addLayout(self.mainwindow_layout)
        self.mainwindow_layout.addLayout(leftmenu_layout)
        self.mainwindow_layout.addWidget(self.overview_frame)
        self.mainwindow_layout.addWidget(self.history_frame)

        self.select_overview()
        self.leftmenu_overview_button.clicked.connect(self.select_overview)
        self.leftmenu_history_button.clicked.connect(self.select_history)

        self.setLayout(box)
        self.show()

    def setup_overview(self):
        c = conn.cursor()
        overview_layout = QVBoxLayout()
        self.overview_frame.setLayout(overview_layout)
        self.overview_frame.hide()
        self.all_frames.append(self.overview_frame)

        query = c.execute("""   SELECT SUM(amount)
                                FROM finances                
                            """)
        bal = query.fetchone()
        accbalance_label = QLabel()
        accbalance_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        accbalance_label.setText('Balance: {}$'.format(bal[0]))
        if bal[0] > 0:
            accbalance_label.setStyleSheet('color: green')
        else:
            accbalance_label.setStyleSheet('color: red')

        table_label = QLabel('Table showing last 5 balance changes')
        table_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        table = QTableWidget()
        table.setMaximumHeight(250)
        table.setRowCount(5)
        table.setColumnCount(4)

        header = table.horizontalHeader()
        for i in range(0, 4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        header2 = table.verticalHeader()
        for i in range(0, 5):
            header2.setSectionResizeMode(i, QHeaderView.Stretch)

        table.setHorizontalHeaderLabels(('Amount', 'In/Out', 'Category', 'Date'))
        query = c.execute("""   SELECT amount, type, category, date
                            FROM finances 
                            ORDER BY date DESC
                            LIMIT 5""")
        querylist = [a for a in query.fetchall()]
        for i in range(0, 5):
            for j in range(0, 4):
                if j == 0:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setData(Qt.EditRole, querylist[i][j])
                    table.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(querylist[i][j])
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(i, j, item)

        overview_layout.addWidget(accbalance_label)
        overview_layout.addWidget(table_label)
        overview_layout.addWidget(table)

    def select_overview(self):
        for frame in self.all_frames:
            frame.hide()
        self.overview_frame.show()
        self.current_widget_label.setText('Overview')

    def setup_history(self):
        c = conn.cursor()
        history_layout = QVBoxLayout()
        self.history_frame.setLayout(history_layout)
        self.history_frame.hide()
        self.all_frames.append(self.history_frame)

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

        self.table = QTableWidget()
        self.table.setMaximumHeight(250)
        self.table.setColumnCount(4)

        header = self.table.horizontalHeader()
        for i in range(0, 4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(('Amount', 'In/Out', 'Category', 'Date'))

        query = c.execute("""   SELECT amount, type, category, date
                                                    FROM finances 
                                                    """)
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

        # self.confirm_button.clicked.connect(self.history_query)
        self.cb1.currentIndexChanged.connect(self.history_query)
        self.cb2.currentIndexChanged.connect(self.history_query)
        self.cb3.currentIndexChanged.connect(self.history_query)
        self.cb4.currentIndexChanged.connect(self.history_query)

        history_layout.addLayout(top_layout)
        history_layout.addWidget(self.table)

    def select_history(self):
        for frame in self.all_frames:
            frame.hide()
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
        where_string = '' + ' AND '.join(crits)
        print(where_string)
        if where_string == '':
            query = c.execute("""   SELECT amount, type, category, date
                                            FROM finances 
                                            """)
            querylist = [a for a in query.fetchall()]
        else:
            query = c.execute("""   SELECT amount, type, category, date
                                            FROM finances 
                                            WHERE
                                            """ + where_string)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    conn = sqlite3.connect('database.db')
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
