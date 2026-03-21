from PyQt6.QtWidgets import QApplication
from screens.login import LoginScreen
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginScreen()
    win.setWindowTitle("Login Screen Test")
    win.show()
    sys.exit(app.exec())

# This test script creates an instance of the LoginScreen and displays it in a window.