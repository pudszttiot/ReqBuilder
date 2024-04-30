import subprocess
import sys

from menu_bar import MenuBar
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QKeySequence, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QShortcut,
    QVBoxLayout,
    QWidget,
)


class WorkerThread(QThread):
    """Worker thread for running pipreqs."""

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

    def run(self):
        try:
            process = subprocess.Popen(
                ["pipreqs", self.directory],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.finished.emit(stdout.decode())
            else:
                self.error.emit(stderr.decode())
        except FileNotFoundError:
            self.error.emit(
                "pipreqs command not found. Make sure pipreqs is installed."
            )
        except Exception as e:
            self.error.emit(str(e))


class ReqBuilder(QMainWindow):
    """Main application window for ReqBuilder."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ReqBuilder")
        self.setGeometry(200, 200, 600, 300)
        self.setWindowIcon(QIcon(r"../Images/builder1.png"))

        self.setStyleSheet("background-color: #E9EBEE; color: #333333;")

        self.initUI()

    def initUI(self):
        """Initialize the user interface."""
        font = QFont()
        font.setPointSize(12)

        self.image_label = QLabel()
        pixmap = QPixmap(r"../Images/reqbuilder_logo2.png")
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

        self.browse_button.clicked.connect(self.browseDirectory)
        self.run_button.clicked.connect(self.runReqBuilder)
        self.clear_button.clicked.connect(self.clearFields)

        # Add menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Create shortcuts
        self.createShortcuts()

    def createShortcuts(self):
        """Create keyboard shortcuts."""
        # Ctrl+O for browse
        browseShortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        browseShortcut.activated.connect(self.browseDirectory)

        # Ctrl+R for run
        runShortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        runShortcut.activated.connect(self.runReqBuilder)

        # Ctrl+C for clear
        clearShortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        clearShortcut.activated.connect(self.clearFields)

    def browseDirectory(self):
        """Open file dialog to select directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.directory_input.setText(directory)

    def runReqBuilder(self):
        """Run pipreqs to generate requirements.txt."""
        directory = self.directory_input.text()
        if directory:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            self.status_label.setText("Running ReqBuilder... This may take a moment.")
            self.createWorkerThread(directory)
        else:
            self.status_label.setText("Please select a directory.")

    def createWorkerThread(self, directory):
        """Create and start worker thread."""
        self.worker_thread = WorkerThread(directory)
        self.worker_thread.finished.connect(self.showSuccessMessage)
        self.worker_thread.error.connect(self.showErrorMessage)
        self.worker_thread.finished.connect(lambda: self.progress_bar.setVisible(False))
        self.worker_thread.error.connect(lambda: self.progress_bar.setVisible(False))
        self.worker_thread.start()

    def showSuccessMessage(self, message):
        """Display success message."""
        self.status_label.setText("requirements.txt file created successfully!")

    def showErrorMessage(self, error):
        """Display error message."""
        self.status_label.setText(f"Error: {error}")

    def clearFields(self):
        """Clear input fields."""
        self.directory_input.clear()
        self.status_label.setText("Ready to run...")
        self.progress_bar.setVisible(False)

    def closeEvent(self, event):
        """Handle application close event."""
        if hasattr(self, "worker_thread") and self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReqBuilder()
    window.show()
    app.aboutToQuit.connect(window.closeEvent)
    sys.exit(app.exec_())
