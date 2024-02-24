import sqlite3
import hashlib
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

class Register(QMainWindow):
    """A class to let user register in the system"""

    def __init__(self) -> None:
        super().__init__()

        # Set up the user interface from Designer
        self.reg_ui = loadUi("reg.ui", self)
        # Connects buttons with screen switcher and registration methods
        self.reg_ui.pushButton_2.clicked.connect(self.switch_to_login)
        self.reg_ui.pushButton.clicked.connect(self.register)

    def switch_to_login(self) -> None:
        """Allows an user to switch to login screen"""
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def hash_password(self, password) -> str:
         """Returns encrypted password"""
         return hashlib.sha256(password.encode()).hexdigest()

    def register(self) -> None:
        """Gets a database ready.
        Then checks for user input and tries to write credentials to DB.
        """

        # Check if email is present in the database
        conn = sqlite3.connect("users.db")
        curs = conn.cursor()
        curs.execute("SELECT email FROM users")
        rows = curs.fetchall()
        emails = [i[0] for i in rows]

        # Reads user input
        self.email = self.reg_ui.lineEdit_2.text()
        self.password = self.reg_ui.lineEdit.text()

        # Control flow depending on registration rules
        if self.email in emails: 
            self.reg_ui.label_4.setStyleSheet("color: red")
            self.reg_ui.label_4.setText("This email is already registered")
        elif "@" not in self.email:
            self.reg_ui.label_4.setStyleSheet("color: red")
            self.reg_ui.label_4.setText("Invalid email")
        elif len(self.password) < 4:
            self.reg_ui.label_4.setStyleSheet("color: red")
            self.reg_ui.label_4.setText("Password must be at least 4 charachters")
        else:
            try: # Writing to DB can fail when it's used concurrently
                hashed_password = self.hash_password(self.password)
                curs.execute("INSERT INTO users (email, password) VALUES (?, ?)", (self.email, hashed_password))
                conn.commit()
                self.reg_ui.label_4.setStyleSheet("color: green")
                self.reg_ui.label_4.setText("Registration successful!")
                conn.close()
            except sqlite3.OperationalError:
                self.reg_ui.label_4.setStyleSheet("color: red")
                self.reg_ui.label_4.setText("Could not save to database. Close if it is open!")
            
            
class Login(QMainWindow):
    """A class to handle user login"""
    def __init__(self) -> None:
        super().__init__()

        # Set up the user interface from Designer
        self.log_ui = loadUi("login.ui", self)

        self.log_ui.pushButton_2.clicked.connect(self.switch_to_register)
        self.log_ui.pushButton.clicked.connect(self.login)

    def switch_to_register(self) -> None:
        """Allows an user to switch to registration screen"""
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def check_password(self, entered_password, stored_password) -> bool: 
        """Returns Boolean value of password validity"""
        return Register.hash_password(self, entered_password) == stored_password
    
    def read_db(self) -> dict:
        """Opens and extracts data from database"""
        conn = sqlite3.connect("users.db")
        curs = conn.cursor() 
        curs.execute("SELECT * FROM users")
        rows = curs.fetchall()
        conn.close()
        return {i[0]:i[1] for i in rows}

    def login(self) -> None:
        """Lets user login to system if registered"""

        # Reads user input
        self.email = self.log_ui.lineEdit_2.text()
        self.password = self.log_ui.lineEdit_3.text()

        # Checks login rules and tries to login
        if self.email not in self.read_db():
            self.log_ui.label_4.setStyleSheet("color: red")
            self.log_ui.label_4.setText("No such email found!")
        elif not self.check_password(self.password, self.read_db()[self.email]):
            self.log_ui.label_4.setStyleSheet("color: red")
            self.log_ui.label_4.setText("Password is incorrect!")
        else:
            try: # Catches any exception (needs testing)
                self.log_ui.label_4.setStyleSheet("color: green")
                self.log_ui.label_4.setText("Login successful!")
            except Exception as e:
                print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    regWindow = Register()
    logWindow = Login()
    widget.addWidget(regWindow)
    widget.addWidget(logWindow)

    widget.setFixedHeight(400)
    widget.setFixedWidth(600)
    widget.setWindowTitle("TBC Academy")
    widget.setWindowIcon(QIcon("resources/tbcicon.png"))
    widget.show()

    sys.exit(app.exec_())