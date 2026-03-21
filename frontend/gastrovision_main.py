import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette

# Import styles and screens
from styles import QSS
from screens.login import LoginScreen
from screens.dashboard import DashboardScreen
from screens.analysis import AnalysisScreen
from screens.results import ResultsScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GASTROVISION V2.0 - GI Disease Prediction Analysis")
        self.resize(1200, 800)
        self.setStyleSheet(QSS)
        
        # --- Central Widget ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # --- Header ---
        self.header = QWidget()
        self.header.setObjectName("Header")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        app_title = QLabel("GASTROVISION V2.0")
        app_title.setObjectName("AppTitle")
        header_layout.addWidget(app_title)
        
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(20, 0, 20, 0)
        for text in ["File", "View", "Options", "Help"]:
            btn = QPushButton(text)
            btn.setFlat(True)
            btn.setStyleSheet("border: none; color: #2e3334; font-weight: bold; text-decoration: underline;")
            nav_layout.addWidget(btn)
        header_layout.addLayout(nav_layout)
        header_layout.addStretch()
        
        self.main_layout.addWidget(self.header)
        
        # --- Body ---
        self.body = QWidget()
        self.body_layout = QHBoxLayout(self.body)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 10)
        
        nav_title = QLabel("SYSTEM NAV")
        nav_title.setStyleSheet("color: #4b53bc; font-weight: 900; font-size: 18px;")
        sidebar_layout.addWidget(nav_title)
        
        sidebar_layout.addWidget(QLabel("V-0.98 BETA"))
        sidebar_layout.addSpacing(20)
        
        self.dash_btn = QPushButton("Dashboard")
        self.dash_btn.setProperty("class", "SidebarButton")
        self.dash_btn.clicked.connect(lambda: self.switch_view(1))
        sidebar_layout.addWidget(self.dash_btn)
        
        self.analysis_btn = QPushButton("Analysis")
        self.analysis_btn.setProperty("class", "SidebarButton")
        self.analysis_btn.clicked.connect(lambda: self.switch_view(2))
        sidebar_layout.addWidget(self.analysis_btn)
        
        self.results_btn = QPushButton("Results")
        self.results_btn.setProperty("class", "SidebarButton")
        self.results_btn.clicked.connect(lambda: self.switch_view(3))
        sidebar_layout.addWidget(self.results_btn)
        
        sidebar_layout.addStretch()
        
        status_box = QFrame()
        status_box.setStyleSheet("background-color: #f3f4f4; border: 2px solid #5f5f5f;")
        status_layout = QVBoxLayout(status_box)
        status_layout.addWidget(QLabel("SYSTEM STATUS"))
        led_layout = QHBoxLayout()
        led = QWidget()
        led.setFixedSize(10, 10)
        led.setStyleSheet("background-color: #22c55e; border-radius: 5px;")
        led_layout.addWidget(led)
        led_layout.addWidget(QLabel("DRIVE_ONLINE: 100%"))
        status_layout.addLayout(led_layout)
        sidebar_layout.addWidget(status_box)
        
        self.body_layout.addWidget(self.sidebar)
        
        # Main View Area (Stacked Widget)
        self.stack = QStackedWidget()
        self.stack.setObjectName("MainContent")
        
        # Initialize Screens
        self.login_screen = LoginScreen()
        self.dashboard_screen = DashboardScreen()
        self.analysis_screen = AnalysisScreen()
        self.results_screen = ResultsScreen()
        
        # Add to Stack
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.dashboard_screen)
        self.stack.addWidget(self.analysis_screen)
        self.stack.addWidget(self.results_screen)
        
        # Connect Signals
        self.login_screen.login_success.connect(lambda: self.switch_view(1))
        
        self.body_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.body)
        
        # --- Footer ---
        footer = QWidget()
        footer.setObjectName("Footer")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(0)
        
        footer_layout.addWidget(QLabel("READY - SYSTEM_OK: 200", objectName="FooterLabel"))
        footer_layout.addWidget(QLabel("Line 1, Col 1", objectName="FooterLabel"))
        footer_layout.addWidget(QLabel("OVR", objectName="FooterLabel"))
        footer_layout.addStretch()
        footer_layout.addWidget(QLabel("SERVER_SYNC: ACTIVE"))
        
        self.main_layout.addWidget(footer)
        
        # Initial State: Hide sidebar and header for login
        self.sidebar.hide()
        self.header.hide()

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        
        # Show/Hide UI elements based on view
        if index == 0: # Login
            self.sidebar.hide()
            self.header.hide()
        else:
            self.sidebar.show()
            self.header.show()
            
        # Update sidebar button states
        self.dash_btn.setProperty("active", "true" if index == 1 else "false")
        self.analysis_btn.setProperty("active", "true" if index == 2 else "false")
        self.results_btn.setProperty("active", "true" if index == 3 else "false")
        
        # Refresh styles to apply "active" property
        self.dash_btn.style().unpolish(self.dash_btn)
        self.dash_btn.style().polish(self.dash_btn)
        self.analysis_btn.style().unpolish(self.analysis_btn)
        self.analysis_btn.style().polish(self.analysis_btn)
        self.results_btn.style().unpolish(self.results_btn)
        self.results_btn.style().polish(self.results_btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
