import urllib
from urllib import request

import pyowm
from PyQt5 import QtWidgets, QtCore, QtGui
from bs4 import BeautifulSoup



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            # noinspection PyArgumentList
            QtWidgets.QApplication.instance().setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

        if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            # noinspection PyArgumentList
            QtWidgets.QApplication.instance().setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

        self.setStyleSheet("background-color: black")

        self.root_container = QtWidgets.QWidget()

        self.left_container = QtWidgets.QWidget()
        self.left_container_layout = QtWidgets.QVBoxLayout()
        self.left_container_layout.setAlignment(QtCore.Qt.AlignTop)

        self.right_container = QtWidgets.QWidget()
        self.right_container_layout = QtWidgets.QVBoxLayout()
        self.right_container_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        # Create widgets
        self.left_container_layout.addWidget(self.clock())
        self.left_container_layout.addWidget(self.meal())

        self.right_container_layout.addWidget(self.weather())
        self.right_container_layout.addWidget(self.farm())

        self.left_container.setLayout(self.left_container_layout)
        self.right_container.setLayout(self.right_container_layout)

        root_layout = QtWidgets.QHBoxLayout()
        root_layout.addWidget(self.left_container)
        root_layout.addWidget(self.right_container)
        self.root_container.setLayout(root_layout)

        self.setCentralWidget(self.root_container)

    def clock(self) -> QtWidgets.QWidget:
        # creating a vertical layout

        # creating a label object
        label = QtWidgets.QLabel("00:00")
        label.setStyleSheet("color: white")

        label2 = QtWidgets.QLabel("Unknown")
        label2.setStyleSheet("color: white; font-size: 32px")

        # setting centre alignment to the label
        # self.label.setAlignment(QtCore.Qt.AlignCenter)

        # adding label to the layout
        self.left_container_layout.addWidget(label)

        # setting the layout to main window
        self.root_container.setLayout(self.left_container_layout)

        # creating a timer object
        timer = QtCore.QTimer(self)

        # adding action to timer
        timer.timeout.connect(lambda: self.update_clock(label, label2))

        # update the timer every second
        timer.start(1000)
        p = QtWidgets.QWidget()
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(label2)
        lay.addWidget(label)

        p.setLayout(lay)
        return p

    @staticmethod
    def update_clock(label: QtWidgets.QLabel, l2: QtWidgets.QLabel):
        # getting current time
        current_time = QtCore.QTime.currentTime()
        current_date = QtCore.QDate.currentDate()

        # converting QTime object to string
        label_time = current_time.toString('hh:mm')
        label2_time = current_date.toString('dddd, MMMM d')

        # showing it to the label
        label.setText(label_time)

        l2.setText(label2_time)

    @staticmethod
    def weather() -> QtWidgets.QWidget:
        # TODO: Update
        _key = "b7dfdf88e34dc2fb2dea1945c4010f09"

        owm = pyowm.OWM(_key)

        weather = owm.weather_manager().weather_at_place("ChunCheon")

        # status = str(weather.to_dict()["weather"]["status"])
        temperature = float(weather.to_dict()["weather"]["temperature"]["temp"]) - 273.15
        temperature = int(temperature)

        web_icon = "http://openweathermap.org/img/wn/" + weather.to_dict()["weather"]["weather_icon_name"] + "@4x.png"
        icon = QtGui.QPixmap()
        icon.loadFromData(urllib.request.urlopen(web_icon).read())
        icon = icon.scaled(128, 128)

        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(icon)
        # print(web_icon)
        icon_label.setStyleSheet("color: white")

        temp_label = QtWidgets.QLabel(str(temperature) + "°C")
        temp_label.setStyleSheet("color: white")

        lay = QtWidgets.QHBoxLayout()
        lay.setAlignment(QtCore.Qt.AlignCenter)
        p = QtWidgets.QWidget()

        lay.addWidget(icon_label)
        lay.addWidget(temp_label)

        p.setLayout(lay)

        return p

    @staticmethod
    def meal() -> QtWidgets.QWidget:
        html: bytes = urllib.request.urlopen("http://kanggo.net/main.do").read()
        soup = BeautifulSoup(html.decode(), 'lxml')

        m: str = soup.find(attrs={"class": "meal_list"}).text
        m = '\n'.join(m.split())

        label = QtWidgets.QLabel("\n\n●오늘의 급식:\n"+m)
        label.setStyleSheet("font-size: 24px")

        return label

    @staticmethod
    def farm() -> QtWidgets.QWidget:
        p = QtWidgets.QWidget()
        p.setStyleSheet("color: white; font-size: 24px")

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        top_label = QtWidgets.QLabel("스마트팜")
        top_label.setStyleSheet("font-size: 32px")

        # TODO: Gather sensor values of smart farm via socket communication
        temp = QtWidgets.QLabel("온도: NaN°C")

        layout.addWidget(top_label)
        layout.addWidget(temp)

        p.setLayout(layout)

        return p
