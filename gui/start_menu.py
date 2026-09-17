from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from gui.lights_menu_ui import LightsWindow
from storage import load_scores, delete_score


class StartMenu(QMainWindow):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("gui/F1_1stUI.ui", self)
        self.app = app

        self.current_user = {"username": "player"}
        self.lights_menu = None
        self.start_game.clicked.connect(self.start)
     
    def start(self):
        self.hide()
        self.lights_menu = LightsWindow(self)
        self.lights_menu.show()
        self.lights_menu.start()

    def show_start_menu(self):
        if self.lights_menu:
            self.lights_menu.close()
            self.lights_menu = None
        self.show()