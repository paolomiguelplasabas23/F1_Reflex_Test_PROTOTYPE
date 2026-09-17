import sys
from PyQt6.QtWidgets import QApplication
from gui.start_menu import StartMenu

app = QApplication(sys.argv)
window = StartMenu(app)
window.show()
sys.exit(app.exec())
