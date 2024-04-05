import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QProgressBar
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

    def run(self):
        try:
            process = subprocess.Popen(["pipreqs", self.directory], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.finished.emit(stdout.decode())
            else:
                self.error.emit(stderr.decode())
        except Exception as e:
            self.error.emit(str(e))

class ReqBuilder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("‍ReqBuilder")
        self.setGeometry(200, 200, 600, 300)
        self.setWindowIcon(QIcon(r"../Images/builder1.png"))

        self.setStyleSheet("background-color: #E9EBEE; color: #333333;")

        font = QFont()
        font.setPointSize(12)

        self.image_label = QLabel()
        pixmap = QPixmap(r"../Images/reqbuilder2.png")  # Replace "your_image.png" with your image path
        self.image_label.setPixmap(pixmap)

        self.directory_label = QLabel("Select Directory:")
        self.directory_label.setFont(font)
        self.directory_input = QLineEdit()
        self.directory_input.setFont(font)
        self.directory_input.setPlaceholderText("Click browse to select directory")
        self.browse_button = QPushButton("Browse")
        self.browse_button.setFont(font)
        self.run_button = QPushButton("Run ‍ReqBuilder")
        self.run_button.setFont(font)
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFont(font)
        self.status_label = QLabel("Ready to run...")
        self.status_label.setFont(font)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.directory_input)
        directory_layout.addWidget(self.browse_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.clear_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)  # Add image label
        layout.addWidget(self.directory_label)
        layout.addLayout(directory_layout)
        layout.addSpacing(10)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.setContentsMargins(20, 20, 20, 20)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.browse_button.setStyleSheet("background-color: #007bff; color: #ffffff;")
        self.run_button.setStyleSheet("background-color: #28a745; color: #ffffff;")
        self.clear_button.setStyleSheet("background-color: #dc3545; color: #ffffff;")

        self.browse_button.clicked.connect(self.browse_directory)
        self.run_button.clicked.connect(self.run_pipreqs)
        self.clear_button.clicked.connect(self.clear_fields)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.directory_input.setText(directory)

    def run_pipreqs(self):
        directory = self.directory_input.text()
        if directory:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.status_label.setText("Running ReqBuilder... This may take a moment.")
            self.worker_thread = WorkerThread(directory)
            self.worker_thread.finished.connect(self.show_success_message)
            self.worker_thread.error.connect(self.show_error_message)
            self.worker_thread.finished.connect(lambda: self.progress_bar.setVisible(False))
            self.worker_thread.error.connect(lambda: self.progress_bar.setVisible(False))
            self.worker_thread.start()
        else:
            self.status_label.setText("Please select a directory.")

    def show_success_message(self):
        self.status_label.setText("requirements.txt file created successfully!")

    def show_error_message(self, error):
        self.status_label.setText(f"Error: {error}")

    def clear_fields(self):
        self.directory_input.clear()
        self.status_label.setText("Ready to run...")
        self.progress_bar.setVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReqBuilder()
    window.show()
    sys.exit(app.exec_())
