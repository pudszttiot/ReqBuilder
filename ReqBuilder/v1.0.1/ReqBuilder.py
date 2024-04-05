import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QProgressBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

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

class PipreqsGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pipreqs GUI")
        self.setGeometry(100, 100, 500, 300)
        self.setWindowIcon(QIcon('icon.png'))

        font = QFont()
        font.setPointSize(10)

        self.directory_label = QLabel("Directory:")
        self.directory_label.setFont(font)
        self.directory_input = QLineEdit()
        self.directory_input.setFont(font)
        self.browse_button = QPushButton("Browse")
        self.browse_button.setFont(font)
        self.run_button = QPushButton("Run pipreqs")
        self.run_button.setFont(font)
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFont(font)
        self.output_label = QLabel("Output:")
        self.output_label.setFont(font)
        self.output_display = QTextEdit()
        self.output_display.setFont(font)
        self.output_display.setReadOnly(True)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.directory_input)
        directory_layout.addWidget(self.browse_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.clear_button)

        layout = QVBoxLayout()
        layout.addWidget(self.directory_label)
        layout.addLayout(directory_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_display)
        layout.addWidget(self.progress_bar)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

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
            self.statusBar().showMessage("Running pipreqs... This may take a moment.")
            self.worker_thread = WorkerThread(directory)
            self.worker_thread.finished.connect(self.update_output)
            self.worker_thread.error.connect(self.show_error)
            self.worker_thread.finished.connect(lambda: self.progress_bar.setVisible(False))
            self.worker_thread.error.connect(lambda: self.progress_bar.setVisible(False))
            self.worker_thread.finished.connect(lambda: self.statusBar().showMessage("pipreqs completed successfully!"))
            self.worker_thread.error.connect(lambda: self.statusBar().showMessage("Error occurred while running pipreqs."))
            self.worker_thread.start()
        else:
            self.statusBar().showMessage("Please select a directory.")

    def update_output(self, output):
        self.output_display.setText(output)

    def show_error(self, error):
        self.output_display.setText(f"Error: {error}")

    def clear_fields(self):
        self.directory_input.clear()
        self.output_display.clear()
        self.statusBar().clearMessage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipreqsGUI()
    window.show()
    sys.exit(app.exec_())
