from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from database import DB

class LoginPage(QMainWindow):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("ui_designs/login_page_ui.ui", self)
        self.app = app

        self.pushButton.clicked.connect(self.handle_login)
        self.pushButton_2.clicked.connect(self.go_register)

    def handle_login(self):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Missing", "Enter username and password.")
            return

        user = DB.login_player(username, password)
        if user is None:
            QMessageBox.warning(self, "Login failed", "Invalid credentials.")
            return

        self.app.current_user = user
        self.app.show_start_menu()

    def go_register(self):
        self.app.show_register()
