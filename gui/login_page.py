from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from features.auth import login

class LoginPage(QMainWindow):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("ui_designs/login_page_ui.ui", self)
        self.app = app

        self.pushButton.clicked.connect(self.handle_login)
        self.pushButton_2.clicked.connect(self.go_register)

    def handle_login(self):
        username = self.lineEdit.text().strip()
        

        if not username:
            QMessageBox.warning(self, "Missing", "Enter username")
            return

        user = login(username)
        if user is None:
            QMessageBox.warning(self, "Login failed", "Username not found.")
            return

        self.app.current_user = user
        self.app.show_start_menu()

    def go_register(self):
        self.app.show_register()
