from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt

class DashboardScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("SYSTEM DASHBOARD")
        header.setStyleSheet("font-size: 24px; font-weight: 900; color: #4b53bc;")
        layout.addWidget(header)
        
        # Stats Grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        stats = [
            ("TOTAL CASES", "1,284", "#4b53bc"),
            ("PENDING ANALYSIS", "12", "#f59e0b"),
            ("SYSTEM ACCURACY", "98.4%", "#10b981"),
            ("UPTIME", "42D 12H", "#6366f1")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = QFrame()
            card.setProperty("class", "StatCard")
            card.setStyleSheet(f"border-left: 4px solid {color};")
            card_layout = QVBoxLayout(card)
            
            val_label = QLabel(value)
            val_label.setProperty("class", "StatValue")
            val_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: 900;")
            card_layout.addWidget(val_label)
            
            lbl_label = QLabel(label)
            lbl_label.setProperty("class", "StatLabel")
            card_layout.addWidget(lbl_label)
            
            stats_grid.addWidget(card, i // 2, i % 2)
            
        layout.addLayout(stats_grid)
        
        # Activity Feed
        feed_box = QFrame()
        feed_box.setStyleSheet("""
            background-color: #f3f4f4;
            border: 2px solid;
            border-top-color: #5f5f5f;
            border-left-color: #5f5f5f;
            border-bottom-color: #ffffff;
            border-right-color: #ffffff;
        """)
        feed_layout = QVBoxLayout(feed_box)
        feed_layout.addWidget(QLabel("SYSTEM ACTIVITY LOG"))
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(5)
        
        activities = [
            ("[10:42:01] CASE_REF: 8829-X - ANALYSIS_COMPLETE", "#10b981"),
            ("[10:38:15] SYSTEM_UPDATE: NEURAL_KERNEL_V2.1", "#4b53bc"),
            ("[10:35:44] USER_LOGIN: DR_SMITH_88", "#5f5f5f"),
            ("[10:30:12] CASE_REF: 4412-B - UPLOAD_SUCCESS", "#10b981"),
            ("[10:25:00] SYSTEM_BOOT: OK", "#4b53bc")
        ]
        
        for text, color in activities:
            item = QLabel(text)
            item.setStyleSheet(f"color: {color}; font-family: 'Courier New'; font-size: 11px; font-weight: bold;")
            scroll_layout.addWidget(item)
            
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        feed_layout.addWidget(scroll)
        
        layout.addWidget(feed_box, 1)
        
        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.addWidget(QPushButton("REFRESH SYSTEM"))
        actions_layout.addWidget(QPushButton("EXPORT LOGS"))
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
