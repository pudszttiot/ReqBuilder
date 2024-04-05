import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit
from PyQt5.QtGui import QIcon, QFont

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
            try:
                output = subprocess.check_output(["pipreqs", directory], stderr=subprocess.STDOUT, text=True)
                self.output_display.setText(output)
                self.statusBar().showMessage("pipreqs completed successfully!", 3000)
            except subprocess.CalledProcessError as e:
                self.output_display.setText(f"Error: {e.output}")
                self.statusBar().showMessage("Error occurred while running pipreqs.", 3000)
        else:
            self.statusBar().showMessage("Please select a directory.", 3000)

    def clear_fields(self):
        self.directory_input.clear()
        self.output_display.clear()
        self.statusBar().clearMessage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipreqsGUI()
    window.show()
    sys.exit(app.exec_())
