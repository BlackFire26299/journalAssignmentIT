from PyQt6.QtWidgets import QApplication, QListWidget, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QListWidget Clear Example")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.list_widget = QListWidget()
        self.list_widget.addItems(["Item 1", "Item 2", "Item 3", "Item 4"])
        layout.addWidget(self.list_widget)

        clear_button = QPushButton("Clear List")
        clear_button.clicked.connect(self.clear_list_widget)
        layout.addWidget(clear_button)

    def clear_list_widget(self):
        """Clears all items from the QListWidget."""
        self.list_widget.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())