import sys

from PyQt6.QtWidgets import QApplication
from gui.start_menu import StartMenu

def main() -> int:
    app = QApplication(sys.argv)
    window = StartMenu(app)
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())