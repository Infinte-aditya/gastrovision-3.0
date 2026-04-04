from PyQt6.QtCore import Qt, QSize

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QProgressBar, QFrame, QGridLayout, QFileDialog # Add QFileDialog
)

import os

import requests
from PyQt6.QtCore import QThread, pyqtSignal

class AnalysisWorker(QThread):
    # Signals to talk back to the UI
    finished = pyqtSignal(dict)  # Sends the JSON result
    error = pyqtSignal(str)     # Sends error message

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        try:
            url = "http://127.0.0.1:8000/predict"
            with open(self.video_path, 'rb') as f:
                files = {'file': (os.path.basename(self.video_path), f, 'video/mp4')}
                response = requests.post(url, files=files, timeout=300)

                
            if response.status_code == 200:
                self.finished.emit(response.json())
            else:
                self.error.emit(f"Server Error: {response.status_code}")
        except Exception as e:
            self.error.emit(str(e))



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
        self.upload_btn = QPushButton("Upload Video")
        self.upload_btn.clicked.connect(self.get_video_file)
        btn_layout.addWidget(self.upload_btn)
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
        self.pbar = QProgressBar()
        self.pbar.setValue(5)
        self.pbar.setFormat("05% INITIALIZING_NEURAL_KERNELS...")
        proc_layout.addWidget(self.pbar)
        self.exec_btn = QPushButton("EXECUTE ANALYSIS SEQUENCE")
        self.exec_btn.clicked.connect(self.start_analysis_thread)
        self.exec_btn.setObjectName("ExecuteBtn")
        proc_layout.addWidget(self.exec_btn)
        layout.addWidget(proc_box)


    def get_video_file(self):
        # Open the Windows/Mac/Linux file picker
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Endoscopy Video", 
            "", 
            "Video Files (*.mp4 *.avi *.mkv);;All Files (*)"
        )

        if file_path:
            self.selected_video_path = file_path
            filename = os.path.basename(file_path)
            
            # Update the UI to show which file is loaded
            # (Assuming you want to change the 'VIDEO PROPERTIES' label)
            print(f"Selected: {self.selected_video_path}")
            self.upload_btn.setText(f"LOADED: {filename}")
            
    def start_analysis(self):
        if hasattr(self, 'selected_video_path'):
            # This is where you will trigger the API call later
            print(f"Ready to analyze: {self.selected_video_path}")
        else:
            print("Please upload a video first!")

        
    def start_analysis_thread(self):
        if not hasattr(self, 'selected_video_path'):
            print("No file selected!")
            return

        # 1. Update UI to "Loading" state
        self.exec_btn.setEnabled(False)
        self.pbar.setRange(0, 0) # Busy/Marquee mode
        self.pbar.setFormat("AI ANALYZING... PLEASE WAIT")

        # 2. Create and start the thread
        self.worker = AnalysisWorker(self.selected_video_path)
        self.worker.finished.connect(self.on_analysis_success)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()

    def on_analysis_success(self, result):
        # Reset UI
        self.pbar.setRange(0, 100)
        self.pbar.setValue(100)
        self.pbar.setFormat("ANALYSIS COMPLETE")
        self.exec_btn.setEnabled(True)
        
        print(f"Backend Result: {result}")
        # TODO: Switch to ResultsScreen and pass 'result'

    def on_analysis_error(self, message):
        self.pbar.setRange(0, 100)
        self.pbar.setFormat("ERROR OCCURRED")
        self.exec_btn.setEnabled(True)
        print(f"Error: {message}")
