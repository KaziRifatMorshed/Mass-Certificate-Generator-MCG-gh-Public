# Desktop and deployment entrypoint
import os
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import version
from mainwindow import MainWindow

# Attach to Windows parent console if launched from CMD or PowerShell
version.setup_windows_console()

app = QApplication(sys.argv)
app.setApplicationName(version.APP_NAME)
app.setApplicationDisplayName(version.APP_DISPLAY_NAME)
app.setOrganizationName(version.ORGANIZATION_NAME)
app.setOrganizationDomain(version.ORGANIZATION_DOMAIN)
app.setApplicationVersion(version.APP_VERSION_STR)

# Global application icon
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra", "MCG_logo.ico")
if not os.path.exists(icon_path):
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extra", "MCG_logo.png")
if os.path.exists(icon_path):
    app.setWindowIcon(QIcon(icon_path))

widget = MainWindow()
widget.show()
sys.exit(app.exec())
