from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt

class ResultsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("DIAGNOSTIC RESULTS")
        header.setStyleSheet("font-size: 24px; font-weight: 900; color: #4b53bc;")
        layout.addWidget(header)
        
        # Results Table
        table_box = QFrame()
        table_box.setProperty("class", "InsetFrame")
        table_layout = QVBoxLayout(table_box)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["CASE_ID", "PATIENT", "DATE", "STATUS"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #5f5f5f;
            }
            QHeaderView::section {
                background-color: #f3f4f4;
                padding: 5px;
                border: 1px solid #5f5f5f;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 10px;
            }
        """)
        
        data = [
            ("8829-X", "John Doe", "2026-03-20", "COMPLETED"),
            ("4412-B", "Sarah Miller", "2026-03-19", "PENDING"),
            ("1234-A", "Robert Brown", "2026-03-18", "COMPLETED"),
            ("5678-C", "Emily Davis", "2026-03-17", "COMPLETED")
        ]
        
        self.table.setRowCount(len(data))
        for row, (cid, pat, date, status) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(cid))
            self.table.setItem(row, 1, QTableWidgetItem(pat))
            self.table.setItem(row, 2, QTableWidgetItem(date))
            status_item = QTableWidgetItem(status)
            if status == "COMPLETED":
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            else:
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            self.table.setItem(row, 3, status_item)
            
        table_layout.addWidget(self.table)
        layout.addWidget(table_box, 1)
        
        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.addWidget(QPushButton("DOWNLOAD PDF REPORT"))
        actions_layout.addWidget(QPushButton("PRINT RESULTS"))
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
