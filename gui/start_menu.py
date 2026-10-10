from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QPushButton

from gui.lights_window import LightsWindow
from gui.login_page import LoginPage
from gui.driver_register_page import RegistrationPage
from gui.leaderboard_window import Leaderboard


class StartMenu(QMainWindow):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("ui_designs/F1_1stUI.ui", self)
        self.app = app

        self.current_user = None
        self.lights_menu = None
        self.login_page = None
        self.register_page = None
        self.leaderboard = None

        self.start_game.clicked.connect(self.start)
        for btn in self.findChildren(QPushButton):
            if "LEADERBOARD" in btn.text().upper():
                btn.clicked.connect(self.show_leaderboard)
                break


    def start(self):
        if self.current_user is None:
            self.show_login()
            return
        self.hide()
        self.lights_menu = LightsWindow(self)
        self.lights_menu.show()
        self.lights_menu.start()

    def show_login(self):
        self.hide()
        self.login_page = LoginPage(self)
        self.login_page.show()

    def show_register(self):
        if self.login_page:
            self.login_page.close()
            self.login_page = None
        self.register_page = RegistrationPage(self)
        self.register_page.show()

    def show_leaderboard(self):
        self.hide()
        self.leaderboard = Leaderboard(self)
        self.leaderboard.show()
    
    def show_start_menu(self):
       for w in (self.lights_menu, self.login_page,
                 self.register_page, self.leaderboard):
           if w:
               w.close()
        
       self.lights_menu = None
       self.login_page = None
       self.register_page = None
       self.leaderboard = None
       self.show()