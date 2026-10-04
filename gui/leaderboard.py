from email.mime import text
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QTableWidgetItem, QWidget
from PyQt6.QtGui import QColor
from database import DB


class Leaderboard(QWidget):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("ui_designs/leaderboard_ui.ui", self)
        self.app = app

        self.backButton.clicked.connect(self.go_back)
        self.load_leaderboard()

    def load_leaderboard(self):
        rows = DB.get_leaderboard()
        self.tableWidget.setRowCount(10)

        for i in range(10):
            if i < len(rows):
                r = rows[i]
                rank = str(r["rank"])
                name = r["fullname"]
                time = f"{r['best_time']} ms"
                rating = DB.rate_reaction(int(r["best_time"]))
                date = r["date_achieved"] or "-"
            else:
                rank = str(i + 1)
                rating = ""
                name = ""
                time = ""
                date = ""

            for col, text in enumerate([rank, rating, name, time, date]):
                item = QTableWidgetItem(text)
                item.setForeground(QColor("white"))
                self.tableWidget.setItem(i, col, item)
            # self.tableWidget.setItem(i, 0, QTableWidgetItem(rank)) 
            # self.tableWidget.setItem(i, 1, QTableWidgetItem(name))
            # self.tableWidget.setItem(i, 2, QTableWidgetItem(time))
            # self.tableWidget.setItem(i, 3, QTableWidgetItem(date))

    def go_back(self):
        self.close()
        self.app.show_start_menu()
            