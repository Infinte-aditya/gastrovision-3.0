from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QProgressBar, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, QSize

class AnalysisScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Patient Strip
        strip = QFrame()
        strip.setProperty("class", "OutsetFrame")
        strip_layout = QHBoxLayout(strip)
        strip_layout.addWidget(QLabel("SELECT PATIENT:"))
        combo = QComboBox()
        combo.addItems(["CASE_REF: 8829-X (John Doe)", "CASE_REF: 4412-B (Sarah Miller)"])
        strip_layout.addWidget(combo, 1)
        strip_layout.addWidget(QPushButton("New Patient"))
        layout.addWidget(strip)
        
        # Video Area
        video_grid = QHBoxLayout()
        video_grid.setSpacing(20)
        
        video_panel = QVBoxLayout()
        video_box = QFrame()
        video_box.setProperty("class", "InsetFrame")
        video_box.setStyleSheet("background-color: black;")
        video_box.setMinimumSize(600, 400)
        video_panel.addWidget(video_box)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("Upload Video"))
        btn_layout.addWidget(QPushButton("Live Capture"))
        video_panel.addLayout(btn_layout)
        
        video_grid.addLayout(video_panel, 2)
        
        inspector = QFrame()
        inspector.setProperty("class", "InsetFrame")
        inspector_layout = QVBoxLayout(inspector)
        inspector_layout.addWidget(QLabel("VIDEO PROPERTIES"))
        
        prop_box = QFrame()
        prop_box.setStyleSheet("background-color: #e5e9e9; border: 1px solid #5f5f5f;")
        prop_layout = QVBoxLayout(prop_box)
        prop_layout.addWidget(QLabel("FPS: 60.0"))
        prop_layout.addWidget(QLabel("RES: 1920x1080"))
        prop_layout.addWidget(QLabel("CODEC: H.264"))
        inspector_layout.addWidget(prop_box)
        
        inspector_layout.addWidget(QLabel("DIAGNOSTIC MODE"))
        diag_grid = QGridLayout()
        diag_grid.addWidget(QPushButton("Tissue Analysis"), 0, 0)
        diag_grid.addWidget(QPushButton("Anomaly Det."), 0, 1)
        diag_grid.addWidget(QPushButton("Colorimetry"), 1, 0)
        diag_grid.addWidget(QPushButton("Edge Detect"), 1, 1)
        inspector_layout.addLayout(diag_grid)
        inspector_layout.addStretch()
        video_grid.addWidget(inspector, 1)
        
        layout.addLayout(video_grid)
        
        # Start Processing
        proc_box = QFrame()
        proc_box.setProperty("class", "OutsetFrame")
        proc_layout = QVBoxLayout(proc_box)
        proc_layout.addWidget(QLabel("START PROCESSING"))
        pbar = QProgressBar()
        pbar.setValue(5)
        pbar.setFormat("05% INITIALIZING_NEURAL_KERNELS...")
        proc_layout.addWidget(pbar)
        exec_btn = QPushButton("EXECUTE ANALYSIS SEQUENCE")
        exec_btn.setObjectName("ExecuteBtn")
        proc_layout.addWidget(exec_btn)
        layout.addWidget(proc_box)
