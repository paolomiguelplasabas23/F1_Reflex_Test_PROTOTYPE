import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

class RegistrationPage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('driver_page.ui', self)
        self.login_button.clicked.connect(self.handle_driver_login)