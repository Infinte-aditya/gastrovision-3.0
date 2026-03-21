# --- Stylesheet ---
QSS = """
QMainWindow {
    background-color: #d5dbdc;
}

QWidget {
    font-family: "Inter", "Segoe UI", sans-serif;
    color: #2e3334;
}

/* 3D Outset Border */
.OutsetFrame {
    background-color: #faf9f9;
    border-top: 2px solid #ffffff;
    border-left: 2px solid #ffffff;
    border-bottom: 2px solid #5f5f5f;
    border-right: 2px solid #5f5f5f;
}

/* 3D Inset Border */
.InsetFrame {
    background-color: #f3f4f4;
    border-top: 2px solid #5f5f5f;
    border-left: 2px solid #5f5f5f;
    border-bottom: 2px solid #ffffff;
    border-right: 2px solid #ffffff;
}

/* Header Title Bar */
#Header {
    background-color: #faf9f9;
    border-bottom: 2px solid #5f5f5f;
}

#AppTitle {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4b53bc, stop:1 #3f46af);
    color: white;
    font-weight: 900;
    padding: 5px 15px;
    text-transform: uppercase;
}

/* Sidebar */
#Sidebar {
    background-color: #f3f4f4;
    border-right: 2px solid #5f5f5f;
    min-width: 220px;
}

.SidebarButton {
    background-color: #faf9f9;
    border: 2px solid;
    border-top-color: #ffffff;
    border-left-color: #ffffff;
    border-bottom-color: #5f5f5f;
    border-right-color: #5f5f5f;
    padding: 10px;
    text-align: left;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 11px;
}

.SidebarButton:hover {
    background-color: #e5e9e9;
}

.SidebarButton[active="true"] {
    background-color: #4b53bc;
    color: white;
    border: none;
}

/* Main Content */
#MainContent {
    background-color: #d5dbdc;
}

/* Buttons */
QPushButton {
    background-color: #faf9f9;
    border: 2px solid;
    border-top-color: #ffffff;
    border-left-color: #ffffff;
    border-bottom-color: #5f5f5f;
    border-right-color: #5f5f5f;
    padding: 8px 15px;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 11px;
}

QPushButton:pressed {
    border-top-color: #5f5f5f;
    border-left-color: #5f5f5f;
    border-bottom-color: #ffffff;
    border-right-color: #ffffff;
    padding-top: 9px;
    padding-left: 16px;
}

QPushButton#ExecuteBtn {
    background-color: #4b53bc;
    color: white;
    font-size: 18px;
    padding: 15px;
}

/* Inputs */
QLineEdit, QComboBox {
    background-color: #ffffff;
    border: 2px solid;
    border-top-color: #5f5f5f;
    border-left-color: #5f5f5f;
    border-bottom-color: #ffffff;
    border-right-color: #ffffff;
    padding: 5px;
}

/* Progress Bar */
QProgressBar {
    border: 2px solid #5f5f5f;
    background-color: #e5e9e9;
    text-align: center;
    font-weight: bold;
    color: black;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4b53bc, stop:1 #3f46af);
}

/* Cards */
.StatCard {
    background-color: #faf9f9;
    border: 2px solid;
    border-top-color: #ffffff;
    border-left-color: #ffffff;
    border-bottom-color: #5f5f5f;
    border-right-color: #5f5f5f;
    padding: 15px;
}

.StatValue {
    font-size: 24px;
    font-weight: 900;
    color: #4b53bc;
}

.StatLabel {
    font-size: 10px;
    font-weight: bold;
    text-transform: uppercase;
    color: #5f5f5f;
}
"""
