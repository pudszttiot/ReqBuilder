import os  # Importing os for path operations
import subprocess
import sys

from menu_bar import MenuBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal  # Import Qt for thread handling
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

    def run(self):
        try:
            with subprocess.Popen(
                ["pipreqs", self.directory],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
                bufsize=1,  # Buffering the output
                universal_newlines=True,  # Using text mode to avoid decoding overhead
            ) as process:
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    self.finished.emit(stdout)
                else:
                    self.error.emit(stderr)
        except Exception as e:
            self.error.emit(str(e))


class ReqBuilder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ReqBuilder")
        self.setGeometry(200, 200, 600, 300)
        self.setWindowIcon(
            QIcon(os.path.abspath("../Images/builder1.png"))
        )  # Absolute path for icon

        self.setStyleSheet("background-color: #E9EBEE; color: #333333;")

        font = QFont()
        font.setPointSize(12)

        self.image_label = QLabel()
        pixmap = QPixmap(
            os.path.abspath("../Images/reqbuilder_logo2.png")
        )  # Absolute path for image
        self.image_label.setPixmap(pixmap)

        self.directory_label = QLabel("Select Directory:")
        self.directory_label.setFont(font)
        self.directory_input = QLineEdit()
        self.directory_input.setFont(font)
        self.directory_input.setPlaceholderText("Click browse to select directory")
        self.browse_button = QPushButton("Browse")
        self.browse_button.setFont(font)
        self.run_button = QPushButton("Run ReqBuilder")
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
        layout.addWidget(self.image_label)
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

        # Add menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.directory_input.setText(directory)

    def run_pipreqs(self):
        directory = self.directory_input.text()
        if directory:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            self.status_label.setText("Running ReqBuilder... This may take a moment.")
            self.worker_thread = WorkerThread(directory)
            self.worker_thread.finished.connect(
                self.show_success_message, Qt.QueuedConnection
            )  # QueuedConnection to avoid blocking GUI
            self.worker_thread.error.connect(
                self.show_error_message, Qt.QueuedConnection
            )
            self.worker_thread.finished.connect(
                lambda: self.progress_bar.setVisible(False)
            )
            self.worker_thread.error.connect(
                lambda: self.progress_bar.setVisible(False)
            )
            self.worker_thread.start()
        else:
            self.status_label.setText("Please select a directory.")

    def show_success_message(self, message):
        self.status_label.setText("requirements.txt file created successfully!")
        self.progress_bar.setRange(0, 1)  # Resetting progress bar
        self.progress_bar.setValue(1)  # Setting progress to 100%

    def show_error_message(self, error):
        self.status_label.setText(f"Error: {error}")
        self.progress_bar.setRange(0, 1)  # Resetting progress bar
        self.progress_bar.setValue(1)  # Setting progress to 100%

    def clear_fields(self):
        self.directory_input.clear()
        self.status_label.setText("Ready to run...")
        self.progress_bar.setVisible(False)

    def closeEvent(self, event):
        if hasattr(self, "worker_thread") and self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReqBuilder()
    window.show()
    app.aboutToQuit.connect(window.closeEvent)
    sys.exit(app.exec_())
