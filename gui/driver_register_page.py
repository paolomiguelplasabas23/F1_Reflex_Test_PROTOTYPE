from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from features.auth import register

class RegistrationPage(QMainWindow):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("ui_designs/driver_page_ui.ui", self)
        self.app = app

        self.pushButton.clicked.connect(self.handle_register)
        self.pushButton_2.clicked.connect(self.go_login)

    def handle_register(self):
        fullname = self.lineEdit.text().strip()
        username = self.lineEdit_2.text().strip()
        

        ok, message = register(fullname, username)
        if not ok:
            QMessageBox.warning(self, "Error", message)
            return

        pid = register(fullname, username)
        if pid is None:
            QMessageBox.warning(self, "Taken", "Username already exists.")
            return

        QMessageBox.information(self, "Success", "Account created! Please log in.")
        self.app.show_login()

    def go_login(self):
        self.app.show_login()