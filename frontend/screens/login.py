from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

class LoginScreen(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Login Dialog Frame
        dialog = QFrame()
        dialog.setObjectName("LoginDialog")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("""
            #LoginDialog {
                background-color: #faf9f9;
                border: 2px solid;
                border-top-color: #ffffff;
                border-left-color: #ffffff;
                border-bottom-color: #5f5f5f;
                border-right-color: #5f5f5f;
            }
        """)
        
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.setSpacing(0)
        
        # Title Bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4b53bc, stop:1 #3f46af);")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 5, 10, 5)
        
        title_label = QLabel("USER LOGIN")
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        title_bar_layout.addWidget(title_label)
        
        close_btn = QPushButton("X")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("background-color: #faf9f9; border: 1px solid #5f5f5f; font-weight: bold; padding: 0;")
        title_bar_layout.addWidget(close_btn)
        
        dialog_layout.addWidget(title_bar)
        
        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(15)
        
        content_layout.addWidget(QLabel("USERNAME:"))
        self.user_input = QLineEdit()
        self.user_input.setText("DR_SMITH_88")
        content_layout.addWidget(self.user_input)
        
        content_layout.addWidget(QLabel("PASSWORD:"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setText("********")
        content_layout.addWidget(self.pass_input)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        login_btn = QPushButton("LOGIN")
        login_btn.clicked.connect(self.login_success.emit)
        btn_layout.addWidget(login_btn)
        content_layout.addLayout(btn_layout)
        
        dialog_layout.addWidget(content)
        layout.addWidget(dialog)
        
        # Background icons (simulated)
        bg_label = QLabel("GASTRO-DIAG V1.0 - SYSTEM_READY")
        bg_label.setStyleSheet("color: #5f5f5f; font-weight: bold; font-size: 10px;")
        layout.addWidget(bg_label, 0, Qt.AlignmentFlag.AlignCenter)
