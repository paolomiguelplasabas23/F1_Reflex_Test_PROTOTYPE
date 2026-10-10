import time
import random 
from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel, 
    QHBoxLayout, 
    QVBoxLayout,
    QFrame,
    QPushButton,
    QGraphicsDropShadowEffect,
    QWidget 
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor
from database import DB

LIGHT_SIZE = (60, 60)
WINDOW_SIZE = (563, 564)

CONFIG = {
    "light_count": 5,
    "tick_ms": 800,
    "wait_min_ms":1000,
    "wait_max_ms":3000,
}

class LightsWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app

        self.lit_count= 0
        self.go_time = None
        self.can_react = False
        self.sequence_running = False
        self.jump_started = False 
        self.lights = []
        self.setFixedSize(*WINDOW_SIZE)

        # TIMER SETUP

        # WAIT TIMER
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.light_next)
        self.wait_timer = QTimer(self)
        self.wait_timer.setSingleShot(True)
        self.wait_timer.timeout.connect(self.lights_out)

    
        self.setWindowTitle("Lights Out")
        self.setStyleSheet("background-color: black;")
        self.build_ui()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 20, 20, 20)

        frame = QFrame()
        frame.setStyleSheet("background-color: #0a0a0a; border-radius: 12px;")
        outer.addWidget(frame)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        # -------- TOP ROW: back button ---------
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        self.backButton = QPushButton("←")
        self.backButton.setFixedSize(80, 80)
        self.backButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 50px;
                font-weight: 900;
                border: none;
            }
            QPushButton:hover { color: #e10600; }
        """)
        self.backButton.clicked.connect(self.go_back)
        top_row.addWidget(self.backButton)
        top_row.addStretch()
        layout.addLayout(top_row)

        # -------- TITLE ---------
        title = QLabel("LIGHTS OUT")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title.setStyleSheet("color: #e10600; font-size: 26px; font-weight: 900;")
        layout.addWidget(title)

        # -------- GO LABEL ---------
        self.goLabel = QLabel("")
        self.goLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.goLabel.setFixedHeight(34)
        layout.addWidget(self.goLabel)

        # -------- LIGHTS ROW ---------
        lights_row =QHBoxLayout()
        lights_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lights_row.setSpacing(12)

        for _ in range(CONFIG["light_count"]):
            light = QLabel()
            light.setFixedSize(*LIGHT_SIZE)
            self.set_light_off(light)
            self.lights.append(light)
            lights_row.addWidget(light)
        layout.addLayout(lights_row)

        # -------- INFO LABEL ---------
        info = QLabel("PRESS SPACE OR REACT BUTTON AFTER LIGHTS GO OUT")
        info.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        info.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(info)

        layout.addStretch()
        # ------- REACT BUTTON ---------
        react_row = QHBoxLayout()
        react_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reactButton = QPushButton("REACT")
        self.reactButton.setFixedWidth(200)
        self.reactButton.setStyleSheet(
            " QPushButton {"
            "background-color: #e10600;"
            "color: white;"
            "font-weight: 900;"
            "font-size: 18px;"
            "padding: 12px;"
            "border: none;"
            "border-radius: 6px;"
            "}"
        )
        self.reactButton.clicked.connect(self.handle_react)
        react_row.addWidget(self.reactButton)
        layout.addLayout(react_row)

        layout.addStretch()
    # ----------------------------------- LIGHTS ---------------
    def set_light_off(self, light):
        light.setStyleSheet(
            "background-color: #1a0000; border-radius: 30px; border: 2px solid #333;"
        )
        light.setGraphicsEffect(None)

    def start(self):
        self.timer.stop()
        self.wait_timer.stop()
        

        for light in self.lights:
            self.set_light_off(light)

        self.goLabel.setText("")
        self.goLabel.setStyleSheet("")
        self.lit_count = 0
        self.go_time = None
        self.can_react = False
        self.sequence_running = True
        self.jump_started = False

        self.timer.start(CONFIG["tick_ms"])

    def light_next(self):
        if self.lit_count < CONFIG["light_count"]:
            self.set_light_on(self.lights[self.lit_count])
            self.lit_count += 1
        else: 
            self.timer.stop()
            self.wait_timer.start(
                random.randint(CONFIG["wait_min_ms"], CONFIG["wait_max_ms"])
            )

    def set_light_on(self, light):
        light.setStyleSheet(
            "background-color: #e10600; border-radius: 30px; border: 2px solid #333;"
        )
        glow = QGraphicsDropShadowEffect(light)
        glow.setBlurRadius(30)
        glow.setColor(QColor("#e10600"))
        glow.setOffset(0, 0)
        light.setGraphicsEffect(glow)

    def lights_out(self):
        self.go_time = time.time()
        for light in self.lights:
            self.set_light_off(light)
        self.goLabel.setText("GO GO GO!")
        self.goLabel.setStyleSheet("color: #00c853; font-size: 22px; font-weight: 900;")
        self.can_react = True
        self.sequence_running = False

    def handle_react(self):
        # CASE A: IF PLAYER ALREADY JUMP STARTED AND CLICKED SPACE TO RETRY
        if self.jump_started:
            self.start()
            return

        # CASE B: PRESSED TOO EARLY/ JUMP STARTED
        if self.sequence_running or self.wait_timer.isActive():
            self.timer.stop()
            self.wait_timer.stop()
            self.sequence_running = False
            self.jump_started = True
            self.goLabel.setText("JUMP START! PRESS SPACE TO RETRY or REACT BUTTON TO RETRY")
            self.goLabel.setStyleSheet("color: #e10600; font-size: 18px; font-weight: 900;")

            user = getattr(self.app, "current_user", None)
            if user:
                DB.create_session(user["player_id"], "Jump Start")
            return

        # CASE C: VALID REACTION.
        if self.can_react:
            reaction_ms = int((time.time() - self.go_time) * 1000)
            self.goLabel.setText(f"Reaction Time: {reaction_ms} ms")
            self.goLabel.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: 900;")
            self.can_react = False
            
            # add_score(reaction_ms)
            user = getattr(self.app, "current_user", None)
            if user:
                rating = DB.rate_reaction(reaction_ms)
                sid = DB.create_session(user["player_id"], "Valid")
                DB.save_reaction(sid, user["player_id"], reaction_ms, rating)
                DB.refresh_leaderboard()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.handle_react()
        else:
            super().keyPressEvent(event)

    def go_back(self):
        self.timer.stop()
        self.wait_timer.stop()
        self.app.show_start_menu()

    def closeEvent(self, event):
        self.timer.stop()
        self.wait_timer.stop()
        super().closeEvent(event)