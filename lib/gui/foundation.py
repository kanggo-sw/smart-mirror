import sys

from PyQt5 import QtCore, QtWidgets

from lib.gui.mw import MainWindow


class Application(QtCore.QObject):
    """
    Sets up the Qt Application that contains the main window and various controllers.
    """

    def __init__(self):
        super().__init__()

        self.app = QtWidgets.QApplication(sys.argv)

        self.mw = MainWindow()
        if "--full-screen" in sys.argv:
            self.mw.showFullScreen()
        else:
            self.mw.setFixedSize(800, 600)

    @staticmethod
    def restart():
        if hasattr(sys, "frozen"):
            QtCore.QProcess.startDetached(sys.executable)
        else:
            QtCore.QProcess.startDetached(sys.executable, sys.argv)

        sys.exit()

    def start(self):
        return self.app.exec_()
