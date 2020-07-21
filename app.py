import sys

from PyQt5.QtGui import QFont

from lib.gui.foundation import Application


def bootstrap() -> int:
    application_object = Application()
    application_object.app.setFont(QFont("나눔바른펜", 48))
    application_object.app.setStyleSheet("QLabel {color: white}")

    application_object.mw.showMaximized()

    return application_object.start()


if __name__ == '__main__':
    sys.exit(bootstrap())

# Google assistant: https://pypi.org/project/google-assistant-sdk/
