from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QLabel,
    QMainWindow,
    QMenuBar,
    QScrollArea,
    QVBoxLayout,
)


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("ReqBuilder")
        self.setGeometry(550, 350, 800, 600)
        self.setWindowIcon(QIcon(r"../Images/builder1.png"))

        help_text = r"""
            <p style="text-align: center;"><h2><span style="color: #00FF00;">===================================</span></h2>
            <h1><span style="color: #F5F5F5;">🛠 ReqBuilder 🛠</span></h1>
            <h2><span style="color: #FFFFFF;">📝 Version: 2.0.0</span></h2>
            <h2><span style="color: #FFFFFF;">📅 Release Date: April 6, 2024</span></h2>
            <h2><span style="color: #00FF00;">===================================</span></h2>
            
            <p style="text-align: center;">
            <span style="color: #282c34; background-color: yellow;">The
            <strong><span style="color: #000000; background-color: yellow;">ReqBuilder</span></strong>
            <span style="color: #282c34; background-color: yellow;">  is a straightforward application that helps you create a 'requirements.txt' file
            <br>for your Python projects effortlessly. Just select your project directory, run ReqBuilder, and it <br>quickly generates the dependencies list for you.</span></p>


            <p><h3><span style="color: #FF0080;">Here's how to use it:</span></h3></p>
            <ol>
            
                <li>Click the <strong><span style="color: #FF6600;">"Browse"</span></strong> button and choose the directory containing your Python project files.</li>
                <li>Once the directory is selected, click the <strong><span style="color: #FF6600;">"Run ReqBuilder"</span></strong> button.</li>
                <li>ReqBuilder will start processing and generating the 'requirements.txt' file.</li>
                <li>When the process finishes successfully, you'll see a message <br>confirming the creation of the 'requirements.txt' file.</li>
                <li>Use the <strong><span style="color: #FF6600;">"Clear"</span></strong> button to reset the input fields and status message if needed.</li>

            </ol>

            <p><strong>That's it!</strong>...Thank you for using <strong><span style="color: #FFD700;">ReqBuilder!</span></strong></p>

        
            <!-- Add an image here -->
            <p style="text-align: center;"><img src="../Images/reqbuilder_logo2.png" alt="ReqBuilder.png" width="250" height="200" border="1">

            <h6 style="color: #e8eaea;">▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃</h6>
        

        
        <h3><span style="color: #39ff14; background-color: #000000;">╬╬══▲▲▲👽👽 <u>MY CHANNELS</u> 👽👽▲▲▲══╬╬</span></h3></p>
            <br>
            <br>

            <span>
            <img src="../Socials/Github.png" alt="Github.png" width="20" height="20" border="2">
            <a href="https://github.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#e8eaea; margin-right:20px;" onclick="openLink('https://github.com/pudszttiot')">Github Page</a>
            </span> 

            <span>
            <img src="../Socials/Youtube.png" alt="Youtube.png" width="20" height="20" border="2">
            <a href="https://youtube.com/@pudszTTIOT" style="display:inline-block; text-decoration:none; color:#ff0000;" onclick="openLink('https://youtube.com/@pudszTTIOT')">YouTube Page</a>
            </span>

            <span>
            <img src="../Socials/SourceForge.png" alt="SourceForge.png" width="20" height="20" border="2">
            <a href="https://sourceforge.net/u/pudszttiot" style="display:inline-block; text-decoration:none; color:#ee730a;" onclick="openLink('https://sourceforge.net/u/pudszttiot')">SourceForge Page</a>
            </span>
        
            <span>
            <img src="../Socials/Dailymotion.png" alt="Dailymotion.png" width="20" height="20" border="2">
            <a href="https://dailymotion.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#0062ff;" onclick="openLink('https://dailymotion.com/pudszttiot')">Dailymotion Page</a>
            </span>

            <span>
            <img src="../Socials/Blogger.png" alt="Blogger.png" width="20" height="20" border="2">
            <a href="https://pudszttiot.blogspot.com" style="display:inline-block; text-decoration:none; color:#ff5722;" onclick="openLink('https://pudszttiot.blogspot.com')">Blogger Page</a>
            </span>

            <script>
            function openLink(url) {
                QDesktopServices.openUrl(QUrl(url));
            }
            </script>
            
        """

        help_label = QLabel()
        help_label.setAlignment(Qt.AlignLeft)
        help_label.setText(help_text)
        help_label.setOpenExternalLinks(True)  # Allow QLabel to open external links

        # Add a CSS background color
        help_label.setStyleSheet(
            "color: #1E90FF; background-color: #333333; padding: 10px;"
            "border: 2px solid #1E90FF; border-radius: 10px;"
        )

        # Create a scroll area for the help text
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_area.setWidget(help_label)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Add styles to the menu bar
        self.setStyleSheet(
            "QMenuBar { background-color: #333333; color: #ffffff; }"
            "QMenuBar::item:selected { background-color: #555555; color: #ffffff; }"
        )

        file_menu = self.addMenu("&File")
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exit_action)

        # Add Help menu
        help_menu = self.addMenu("&Help")
        how_to_use_action = QAction("&How to Use...", self)
        how_to_use_action.triggered.connect(self.how_to_use)
        help_menu.addAction(how_to_use_action)

    def how_to_use(self):
        dialog = HelpDialog()
        dialog.exec_()


# Example usage
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    menuBar = MenuBar(mainWindow)
    mainWindow.setMenuBar(menuBar)
    mainWindow.show()
    sys.exit(app.exec_())
