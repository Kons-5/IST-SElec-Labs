import math
import threading
#from qtSimulator_1 import Ui_MainWindow
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Signal, QRect, QMetaObject, QCoreApplication
from PySide2 import QtGui
from PySide2.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout, QPushButton, QAction, QLabel, QTextBrowser, \
QMenuBar, QMenu, QStatusBar, QGroupBox, QSlider, QLineEdit, QComboBox
from PySide2.QtWidgets import QMainWindow
from PySide2.QtGui import QPainter, QPixmap, Qt, QPen, QColor, QKeySequence
import time
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from os.path import exists
import os


MICROPYTHON=False
DELAY_START_MS = 1000         # 5000

WIDTH = 240
HEIGHT = 135

DISPLAY_WIDTH  = 135
DISPLAY_HEIGHT = 240

memoria_adc = [0] * 240


class Button():

    def __init__(self):
        self.init_button()

    def init_button(self):
        self.button_clicked = 0
        self.button_clicked_before = 0
        self.time_clicked = 0
        self.time_released = 0
        self.time_released_before = 0

    def press(self, but):
        self.button_clicked = but
        self.time_clicked = self.get_time()
        self.time_released_before = self.time_released
        self.time_released=0

    def release(self, but):
        if but!=self.button_clicked:
            self.init_button()
        else:
            self.time_released = self.get_time()

    def get_time(self):
        if MICROPYTHON:
            return time.time_ms()/1000.
        else:
            return time.time()






# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qtSimulator_1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

#from qtSimulator_1 import Ui_MainWindow

#from PySide2.QtCore import *
#from PySide2.QtGui import *
#from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(926, 604)
        MainWindow.setToolTipDuration(-14)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 50, 240, 135))
        self.label.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 10, 401, 211))
        self.label_2.setPixmap(QPixmap(u"T_Display2.dat"))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(430, 50, 47, 13))
        self.label_3.setStyleSheet(u"color: rgb(134, 134, 134);")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(430, 180, 47, 13))
        self.label_4.setStyleSheet(u"color: rgb(134, 134, 134);")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 250, 401, 191))
        self.groupBox.setStyleSheet(u"background-color: rgb(241, 234, 218);")
        self.horizontalSlider = QSlider(self.groupBox)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(210, 70, 161, 22))
        self.horizontalSlider.setToolTipDuration(-15)
        self.horizontalSlider.setMinimum(2)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setPageStep(5)
        self.horizontalSlider.setValue(5)
        self.horizontalSlider.setSliderPosition(5)
        self.horizontalSlider.setTracking(True)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(30, 70, 81, 16))
        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(140, 70, 41, 20))
        self.lineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit.setReadOnly(True)
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(30, 30, 81, 16))
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(140, 30, 111, 22))
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(30, 110, 81, 16))
        self.horizontalSlider_2 = QSlider(self.groupBox)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setGeometry(QRect(210, 110, 161, 22))
        self.horizontalSlider_2.setMinimum(0)
        self.horizontalSlider_2.setMaximum(10)
        self.horizontalSlider_2.setSliderPosition(5)
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)
        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(140, 110, 41, 20))
        self.lineEdit_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3 = QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(140, 150, 41, 20))
        self.lineEdit_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_3.setReadOnly(True)
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(30, 150, 81, 16))
        self.horizontalSlider_3 = QSlider(self.groupBox)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setGeometry(QRect(210, 150, 161, 22))
        self.horizontalSlider_3.setMinimum(-10)
        self.horizontalSlider_3.setMaximum(10)
        self.horizontalSlider_3.setSliderPosition(0)
        self.horizontalSlider_3.setOrientation(Qt.Horizontal)
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(20, 460, 401, 81))
        self.groupBox_3.setStyleSheet(u"background-color: rgb(241, 234, 218);")
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(40, 20, 41, 20))
        self.lineEdit_4 = QLineEdit(self.groupBox_3)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(80, 20, 101, 20))
        self.lineEdit_4.setReadOnly(False)
        self.pushButton = QPushButton(self.groupBox_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(280, 20, 75, 23))
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(20, 50, 351, 20))
        MainWindow.setCentralWidget(self.centralwidget)
        self.label_2.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.groupBox.raise_()
        self.groupBox_3.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 926, 21))
        self.menuExit = QMenu(self.menubar)
        self.menuExit.setObjectName(u"menuExit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuExit.menuAction())
        self.menuExit.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.comboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label.setText("")
        self.label_2.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Button1", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Button2", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Signal generator simulator", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Frequency (Hz)", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"50", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Waveform", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Sinusoidal", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Square wave", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Triangular", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Amplitude AC (V)", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Offset DC (V)", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Upload main.py to server", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"CODE:", None))
        self.lineEdit_4.setText(QCoreApplication.translate("MainWindow", u"01_Test", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.label_10.setText("")
        self.menuExit.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi





button = Button()

#button_clicked=0
#button_clicked_before=0
#time_clicked=0
#time_released=0
#time_released_before = 0

class TFT():
    NOTHING=0
    BUTTON1_SHORT=11
    BUTTON2_SHORT=21
    BUTTON1_LONG=12
    BUTTON2_LONG=22
    BUTTON1_DCLICK=13
    BUTTON2_DCLICK=23

    BLACK = 0x0000
    BLUE = 0x001F
    RED = 0xF800
    GREEN = 0x07E0
    CYAN = 0x07FF
    MAGENTA = 0xF81F
    YELLOW = 0xFFE0
    WHITE = 0xFFFF
    GREY1=(50 & 0xf8) << 8 | (50 & 0xfc) << 3 | 50 >> 3
    GREY2=(150 & 0xf8) << 8 | (150 & 0xfc) << 3 | 150 >> 3

    win=None

    wifi_logo_x0=0
    wifi_logo_y0=0

    def __init__(self,code=''):

         self.wifi_status = False
         self.code=code

         #self.wifi_logo_x0=0
         #self.wifi_logo_y0=0

         self.work_flag=True
         #self.signal_message=signal_message
         print("Starting T-Display")
#             t = threading.Thread(target=self.mythread,daemon=True)
         t = threading.Thread(target=self.mythread)
         t.daemon = True
         t.start()
         time.sleep(2)
         self.display_set(self.BLACK)
#         self.display_load_image("T_Display1.dat",80,40)
         self.display_load_image("T_Display1.dat",0,0)
         time.sleep(DELAY_START_MS/1000)
            #self.app.processEvents()
         self.display_set(self.BLACK)
         #self.display_load_image("T_Display3.dat", 0, 0)
         #self.display_load_image("T_Display4.dat", 240-31, 0)
         #self.display_load_image("lixo.bmp", 100, 100)
         self.Arial16=Font('arial_16')
         self.wifi_status=self.wifi_start(0)

    def set_wifi_icon(self,x0,y0):
        self.wifi_logo_x0=x0
        self.wifi_logo_y0=y0
        if self.wifi_status:
            self.display_load_image("T_Display4.dat", x0, y0)
        else:
            self.display_load_image("T_Display3.dat", x0, y0)


    def send_mail(self,delta_t,pontos_v,corpo,address):
        self.display_load_image("T_Display5.dat", self.wifi_logo_x0, self.wifi_logo_y0)
        url = "http://raposa.ist.utl.pt/se/SendMail.php"
        print(url)
        csv=""
        for n in range(len(pontos_v)):
            csv += "%.4f,%.3f\n" % (delta_t*n,pontos_v[n])      # Pontos em volt com 3 casas decimais
        dados = {'address':address,
                 'subject':'Points from uOscilloscope',
                 'body':'Points from uOscilloscope: %d points\n\n%s'%(len(pontos_v),corpo),
                 'attachment':csv
                }
        print("dados=",dados)
        try:
            result = requests.post(url,data=dados)
        except:
            print("send_mail(): Failed")
            self.display_load_image("T_Display3.dat", self.wifi_logo_x0, self.wifi_logo_y0)
            return

        if "OK Message" in result.text:
            print("send_mail(): OK")
            self.display_load_image("T_Display4.dat", self.wifi_logo_x0, self.wifi_logo_y0)
        else:
            print("send_mail(): Failed")
            self.display_load_image("T_Display3.dat", self.wifi_logo_x0, self.wifi_logo_y0)
        #print(result.text)

    def get_color(self,r=0, g=0, b=0):
        return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

    def display_set(self, color=BLACK, x=0, y=0, w=WIDTH, h=HEIGHT):
        #print("display_set()",self.win.signal_message)
        self.win.signal_message.emit(('DISPLAY_SET',color,x,y,w,h))

    def display_pixel(self, color=BLACK, x=0, y=0):
        #print("display_pixel()",self.win.signal_message)
        self.win.signal_message.emit(('DISPLAY_PIXEL',color,x,y))

    def display_npixel(self, color, x, y):
        #print("display_npixel()",self.win.signal_message)
        self.win.signal_message.emit(('DISPLAY_NPIXEL',color,x,y))

    def display_line(self, color, x0, y0, x1, y1):
        self.win.signal_message.emit(('DISPLAY_LINE',color,x0,y0,x1,y1))

    def display_nline(self, color, x, y):
        self.win.signal_message.emit(('DISPLAY_NLINE',color,x,y))

    def display_load_image(self,file_name,x=0,y=0):
        self.win.signal_message.emit(('DISPLAY_LOAD_IMAGE',file_name,x,y))

    def display_write_grid(self,x=0,y=0,w=WIDTH,h=HEIGHT,nx=10,ny=8,center_lines=True,line_color=GREY1,border_color=GREY2):
        if nx%2 !=0 or ny%2 !=0:
            return
        dx=(w-1)/nx
        dy=(h-1)/ny
        for n in range(nx+1):
            if n==0 or n==nx:
                self.display_set(border_color, int(x+dx*n+0.5), y, 1, h-1)
            elif n==nx/2:
                if center_lines:
                    self.display_set(border_color, int(x + dx * n + 0.5), y, 1, h - 1)
                else:
                    self.display_set(line_color, int(x + dx * n + 0.5), y, 1, h - 1)
            else:
                self.display_set(line_color, int(x+dx*n+0.5), y, 1, h-1)
        for n in range(ny+1):
            if n==0 or n==ny:
                self.display_set(border_color, x, int(y+dy*n+0.5), w-1, 1)
            elif n==ny/2:
                if center_lines:
                    self.display_set(border_color, x, int(y + dy * n + 0.5), w - 1, 1)
                else:
                    self.display_set(line_color, x, int(y + dy * n + 0.5), w - 1, 1)
            else:
                self.display_set(line_color, x, int(y+dy*n+0.5), w-1, 1)


    def display_write_ch(self, ft, ch, x=0, y=0, foreground=0xffff, background=0x0000):

        image, w, h = ft.get_image(ch, foreground, background)
        self.win.signal_message.emit(('DISPLAY_WRITE_CH', image, foreground, background, x, y, w, h))
        return (h)

    # Aprox. 60ms para Arial_50  e 15ms para Arial_20
    def display_write_str(self, ft, str1, y=0, x=0, foreground=0xffff, background=0x0000):

        htot = 0
        for ch in str1:
            h = self.display_write_ch(ft, ch, y, x, foreground, background)
            y += h
            htot += h

        return (htot)


    def readButton(self):
        time.sleep(0.01)
        global button
        #global button_clicked
        #global button_clicked_before
        #global time_clicked
        #global time_released
        #global time_released_before

        if button.button_clicked!=0 and button.time_released!=0:
            #print(button.time_released-button.time_released_before,button.time_clicked,button.time_released,button.time_released_before)
            #print("-----",button.time_released-button.time_clicked)
            dt=button.time_released-button.time_clicked
            bt=button.button_clicked
            button.button_clicked=0

            for n in range(25):  # 250ms
                if button.button_clicked==bt:
                    button.init_button()
                    if bt==1:
                        return self.BUTTON1_DCLICK
                    else:
                        return self.BUTTON2_DCLICK
                time.sleep(0.01)

            if bt==1:
                if dt<=0.2:
                    return self.BUTTON1_SHORT
                else:
                    return self.BUTTON1_LONG
            elif bt==2:
                if dt<=0.2:
                    return self.BUTTON2_SHORT
                else:
                    return self.BUTTON2_LONG
        return self.NOTHING


    def mythread(self):
        #app = QApplication.instance()
        #if app is None:
        self.app = QApplication(sys.argv)
        self.win = MainWindow()
        self.win.ui.lineEdit_4.setText(QCoreApplication.translate("MainWindow", self.code, None))

        self.win.show()
        print("self.app.exec_() =",self.app.exec_())
        self.work_flag=False

    def working(self):
        return self.work_flag


    #   ADC
    #       v<0.091455V             ADC=0
    #       0.091455V<v<1.89441V    ADC=2271.27*v - 207.72
    #       v>1.89441               ADC=4095
    #
    #   V                       ADC
    #       v = 0.000440282*ADC + 0.091455441
    #


    def read_adc(self, npoints, total_interval):
        time.sleep(total_interval/1000)
        interval = int(total_interval * 1000 / npoints + 0.5)
        if interval < 160 or npoints > 240 or (
                total_interval != 50 and total_interval != 100 and total_interval != 200 and total_interval != 500):
            for n in range(npoints):
                memoria_adc[n] = 0
            return memoria_adc

        waveform=self.win.ui.comboBox.currentText()
        frequency = float(self.win.ui.lineEdit.text())
        vac = float(self.win.ui.lineEdit_2.text())
        vdc = float(self.win.ui.lineEdit_3.text())
        omega=2*math.pi*frequency
        dt=total_interval/npoints*0.001
        if waveform=="Sinusoidal":
            for n in range(npoints):
                vtotal=vdc+vac*math.sin(omega*n*dt)
                vtotal=vtotal/29.3+1          # divisor resistivo + referência de 1V
                if vtotal<0.091455:
                    adctotal=0
                elif vtotal>1.89441:
                    adctotal=4095
                else:
                    adctotal=2271.27*vtotal - 207.72

                memoria_adc[n] = round(adctotal)
        elif waveform == "Square wave":
                for n in range(npoints):
                    if math.asin(math.sin(omega * n * dt))>0:
                        vtotal=vdc+vac
                    else:
                        vtotal=vdc-vac
                    vtotal = vtotal / 29.3 + 1  # divisor resistivo + referência de 1V
                    if vtotal < 0.091455:
                        adctotal = 0
                    elif vtotal > 1.89441:
                        adctotal = 4095
                    else:
                        adctotal = 2271.27 * vtotal - 207.72

                    memoria_adc[n] = round(adctotal)
                    #print(n, ',', vtotal, ',', adctotal, ',', memoria_adc[n])
        elif waveform=="Triangular":
            for n in range(npoints):
                vtotal=vdc+2*vac/math.pi*(math.asin(math.sin(omega*n*dt)))
                vtotal=vtotal/29.3+1          # divisor resistivo + referência de 1V
                if vtotal<0.091455:
                    adctotal=0
                elif vtotal>1.89441:
                    adctotal=4095
                else:
                    adctotal=2271.27*vtotal - 207.72

                memoria_adc[n] = round(adctotal)
                #print(n,',',vtotal,',',adctotal,',',memoria_adc[n])

        return memoria_adc


    def wifi_start(self,timeout):

        try:
            fp = requests.get("http://raposa.ist.utl.pt/se/SendMail.php")
        except:
            return False
        #print(fp.text)

        if "SendMail OK" in fp.text:
            return True
        else:
            return False



    #-------------------------------------


    """    
    def mythread():
    #app = QApplication.instance()
    #if app is None:
    app = QApplication(sys.argv)
    self.win = MainWindow()
    self.win.show()
    app.exec_()


import threading
print("Starting T-Display")
t = threading.Thread(target = mythread)
t.daemon = True
print("antes de t.start()")
t.start()
print("depois de t.start()")
"""




#------------------------------------------


class MainWindow(QMainWindow):

    signal_message = Signal(tuple)

    def __init__(self, *args, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.resize(500, 580)
            self.setWindowTitle("uOscilloscope")
            self.ui.actionExit.triggered.connect(self.closeThisEvent)
            self.ui.label_2.mousePressEvent = self.getPressPos
            self.ui.label_2.mouseReleaseEvent = self.getReleasePos
            self.signal_message.connect(self.display_message)
            self.pixmap = QPixmap(self.ui.label.size())
            self.pixmap.fill(QColor(0,0,0))
#                self.ui.label.setStyleSheet("border: 2px solid white;")
            self.ui.label.setStyleSheet("border: 2px solid rgb(100,40,40);")
            self.ui.label.setGeometry(QRect(60, 50, 240+4, 135+4))
            self.ui.horizontalSlider.valueChanged.connect(self.slider_changed)
            self.ui.horizontalSlider_2.valueChanged.connect(self.slider2_changed)
            self.ui.horizontalSlider_3.valueChanged.connect(self.slider3_changed)
            self.ui.pushButton.clicked.connect(self.submit)
            self.ui.groupBox_3.setTitle("Upload file %s as main.py" % os.path.basename(sys.argv[0]))

    def submit(self) -> None:
        self.ui.label_10.setText('')
        QApplication.processEvents()
        file_name=os.path.basename(sys.argv[0])

        headers = {'User-Agent': 'Mozilla/5.0'}

        if exists(file_name):
            print("argv[0]=", sys.argv[0],"code=",self.ui.lineEdit_4.text())
            files = {
                'type': (None, 'upload'),
                'code': (None, self.ui.lineEdit_4.text()),
                'main': ('main.py', open(file_name, 'rb'), 'text/plain', {'Expires': '0'})
            }
            print(files)
            try:
                response = requests.post('http://raposa.tecnico.ulisboa.pt/se/firmware.php', headers=headers, files=files)
                print("RESPONSE: ", response.text)
                if response.text == "OK":
                    self.ui.label_10.setStyleSheet('color: black')
                    self.ui.label_10.setText("OK: File %s uploaded to server" % file_name)
                else:
                    self.ui.label_10.setStyleSheet('color: red')
                    self.ui.label_10.setText("ERROR: Failed upload %s to server" % file_name)
            except:
                self.ui.label_10.setStyleSheet('color: red')
                self.ui.label_10.setText("OK: Failed to connect do cloud")
        else:
            self.ui.label_10.setStyleSheet('color: red')
            self.ui.label_10.setText("ERROR: File %s does not exist" % file_name)

    def slider_changed(self):
        self.ui.lineEdit.setText(str(self.ui.horizontalSlider.value()*5))

    def slider2_changed(self):
        self.ui.lineEdit_2.setText(str(self.ui.horizontalSlider_2.value()))

    def slider3_changed(self):
        self.ui.lineEdit_3.setText(str(self.ui.horizontalSlider_3.value()))


    def display_message(self,message):
        if len(message)==6 and message[0]=="DISPLAY_SET":
            color=int(message[1])
            x=int(message[2])
            y=int(message[3])
            w=int(message[4])
            h=int(message[5])
            y=HEIGHT-y-h

            qp = QPainter(self.pixmap)
            (r,g,b)=Convert565(color)
            #pen = QPen(QColor(r,g,b), 1)
            #qp.setPen(pen)
            #qp.drawRect(x,y,w,h)
            rect = QRect(x,y,w,h)
            qp.fillRect(rect,QColor(r,g,b))
            #qp.drawLine(10, 10, 50, 10)
            qp.end()
            self.ui.label.setPixmap(self.pixmap)
        elif len(message)==4 and message[0]=="DISPLAY_PIXEL":
            color=int(message[1])
            x=int(message[2])
            y=HEIGHT-int(message[3])-1

            qp = QPainter(self.pixmap)
            (r,g,b)=Convert565(color)
            pen = QPen(QColor(r,g,b), 1)
            qp.setPen(pen)
            qp.drawPoint(x,y)
            qp.end()
            self.ui.label.setPixmap(self.pixmap)

        elif len(message)==4 and message[0]=="DISPLAY_NPIXEL":
            color=int(message[1])
            x=message[2]
            y=message[3]

            qp = QPainter(self.pixmap)
            (r,g,b)=Convert565(color)
            pen = QPen(QColor(r,g,b), 1)
            qp.setPen(pen)
            for n in range(len(x)):
                qp.drawPoint(x[n],HEIGHT-y[n]-1)
            qp.end()
            self.ui.label.setPixmap(self.pixmap)

        elif len(message)==6 and message[0]=="DISPLAY_LINE":
            color=int(message[1])
            x_0=message[2]
            y_0=HEIGHT-message[3]-1
            x_1=message[4]
            y_1=HEIGHT-message[5]-1

            qp = QPainter(self.pixmap)
            (r,g,b)=Convert565(color)
            pen = QPen(QColor(r,g,b), 1)
            qp.setPen(pen)

            """Bresenham's line algorithm"""
            d_x = abs(x_1 - x_0)
            d_y = abs(y_1 - y_0)
            x, y = x_0, y_0
            s_x = -1 if x_0 > x_1 else 1
            s_y = -1 if y_0 > y_1 else 1
            if d_x > d_y:
                err = d_x / 2.0
                while x != x_1:
                    #self.pixel(x, y, color)
                    qp.drawPoint(x, y)
                    err -= d_y
                    if err < 0:
                        y += s_y
                        err += d_x
                    x += s_x
            else:
                err = d_y / 2.0
                while y != y_1:
                    #self.pixel(x, y, color)
                    qp.drawPoint(x, y)
                    err -= d_x
                    if err < 0:
                        x += s_x
                        err += d_y
                    y += s_y
            #self.pixel(x, y, color)
            qp.drawPoint(x, y)

            qp.end()
            self.ui.label.setPixmap(self.pixmap)

        elif len(message)==4 and message[0]=="DISPLAY_NLINE":
            color=int(message[1])
            xn=message[2]
            yn=message[3]
            #x_1=message[4]
            #y_1=HEIGHT-message[5]-1

            qp = QPainter(self.pixmap)
            (r,g,b)=Convert565(color)
            pen = QPen(QColor(r,g,b), 1)
            qp.setPen(pen)

            """Bresenham's line algorithm"""

            for n in range(len(xn)-1):
                x_0=xn[n]
                x_1=xn[n+1]
                y_0 = HEIGHT - yn[n] - 1
                y_1 = HEIGHT - yn[n+1] - 1

                d_x = abs(x_1 - x_0)
                d_y = abs(y_1 - y_0)
                x, y = x_0, y_0
                s_x = -1 if x_0 > x_1 else 1
                s_y = -1 if y_0 > y_1 else 1
                if d_x > d_y:
                    err = d_x / 2.0
                    while x != x_1:
                        #self.pixel(x, y, color)
                        qp.drawPoint(x, y)
                        err -= d_y
                        if err < 0:
                            y += s_y
                            err += d_x
                        x += s_x
                else:
                    err = d_y / 2.0
                    while y != y_1:
                        #self.pixel(x, y, color)
                        qp.drawPoint(x, y)
                        err -= d_x
                        if err < 0:
                            x += s_x
                            err += d_y
                        y += s_y
                #self.pixel(x, y, color)
                qp.drawPoint(x, y)

            qp.end()
            self.ui.label.setPixmap(self.pixmap)

        elif len(message)==4 and message[0]=="DISPLAY_LOAD_IMAGE":
            file_name=message[1]
            x=int(message[2])
            y=int(message[3])
            pix=QPixmap()
            pix.load(file_name)
            pix_img=pix.toImage()
            w=pix.width()
            h=pix.height()
            if w==WIDTH and h==HEIGHT and x==0 and y==0:
                #print("DISPLAY_LOAD_IMAGE (global)", file_name, x, y, pix.width(), pix.height())
                self.ui.label.setPixmap(pix)
            else:
                img=bytearray(pix.width()*pix.height()*2)
                #print("DISPLAY_LOAD_IMAGE (parcial)", file_name, x, y, pix.width(), pix.height())
                qp = QPainter(self.pixmap)
                ptr = 0
                for ny in range(h):
                    for nx in range(w):
                        #rect = QRect(ny + y, w - nx - 1 + x, 1, 1)
                        c = pix_img.pixel(nx,ny)
                        qp.setPen(QColor(c))
#                        qp.drawPoint(x+nx,y-HEIGHT-1+ny)
                        qp.drawPoint(x+nx,HEIGHT-y+ny-h)
                        ptr += 2
                qp.end()
                self.ui.label.setPixmap(self.pixmap)



        elif len(message)==8 and message[0]=="DISPLAY_WRITE_CH":
            image = message[1]
            foreground = int(message[2])
            background = int(message[3])
            w = int(message[6])
            h = int(message[7])
            y = int(message[4])
            x = int(message[5])   #self.pixmap.height() - int(message[5])+1
            x = self.pixmap.height() - int(message[5]) - w

            qp = QPainter(self.pixmap)
            (r, g, b) = Convert565(foreground)
            fore_color = QColor(r, g, b)
            (r, g, b) = Convert565(background)
            back_color = QColor(r, g, b)

            ptr=0
            for ny in range(h):
                for nx in range(w):
                    rect = QRect(ny+y, w-nx-1+x, 1, 1)
                    qp.fillRect(rect, fore_color)
                    if image[ptr]:
                        qp.fillRect(rect, fore_color)
                    else:
                        qp.fillRect(rect, back_color)
                    ptr+=2


            qp.end()
            self.ui.label.setPixmap(self.pixmap)

            """
            rect = QRect(x, y, w, h)
            qp.fillRect(rect, QColor(r, g, b))
            # qp.drawLine(10, 10, 50, 10)
            qp.end()
            self.ui.label.setPixmap(self.pixmap)

            for ny in range(h):
                for nx in range(w):

"""


    def getPressPos(self, event):

        global button
        x = event.pos().x()
        y = event.pos().y()
        if x>=337 and x<=377 and y>=31 and y<=59:
            button.press(1)
        elif x>=337 and x<=377 and y>=160 and y<=187:
            button.press(2)


    def getReleasePos(self, event):

        global button
        x = event.pos().x()
        y = event.pos().y()
        if x >= 337 and x <= 377 and y >= 31 and y <= 59:
            button.release(1)
        elif x >= 337 and x <= 377 and y >= 160 and y <= 187:
            button.release(2)



    """        
    def getPressPos(self, event):
        global button_clicked
        global time_clicked
        global time_released
        global time_released_before

        x = event.pos().x()
        y = event.pos().y()
        if x>=337 and x<=377 and y>=31 and y<=59:
            button_clicked=1
            time_clicked=time.time()
            time_released_before=time_released
            time_released=0
        elif x>=337 and x<=377 and y>=160 and y<=187:
            button_clicked=2
            time_clicked=time.time()
            time_released_before=time_released
            time_released=0


    def getReleasePos(self, event):
        global button_clicked
        global time_clicked
        global time_released
        global time_released_before

        x = event.pos().x()
        y = event.pos().y()
        if x >= 337 and x <= 377 and y >= 31 and y <= 59 and button_clicked==1:
            time_released = time.time()
        elif x >= 337 and x <= 377 and y >= 160 and y <= 187 and button_clicked==2:
            time_released = time.time()
    """

    def closeThisEvent(self, event):
        print("Exit program")
        self.close()
    #    self.destroy()
    #    sys.exit(0)





def Convert565(color):
    return ((color >> 11) & 0b011111)<<3, ((color >> 5) & 0b0111111)<<2, (color & 0b011111) << 3

class Font:
    def __init__(self, name):
        self.dictFont = {}
        tmp = name.split('_')
        self.name = tmp[0]
        if len(tmp) == 2:
            self.npix = tmp[1]
        else:
            self.npix = 1
        del tmp
        #print(".........................", "prvDisplay.fonts.", self.name, self.npix)
#        ft = __import__("prvDisplay.fonts." + name, globals(), locals(), ['_font'], 0)
        ft = __import__( name, globals(), locals(), ['_font'], 0)
        #print(".........................", "prvDisplay.fonts.", self.name, self.npix, len(ft._font))
        self.font = ft
        # print("Font: Font name [%s] imported" % self.name)

    def get_pix(self, ch):
        # (p,w,h)=self.font.get_ch(ch)
        # print(w,h,''.join('{:02x}'.format(x) for x in bytes(p)))
        return (self.font.get_ch(ch))

    def get_image(self, ch, foreground, background):

        #       if (ch.isdigit() or ch=='.') and ch in self.dictFont:
        #           #print(">>>>>>>>>>>>>",ch,"EXISTE")
        #           return(self.dictFont[ch][0],self.dictFont[ch][1],self.dictFont[ch][2])
        #       else:
        # print(">>>>>>>>>>>>>",ch,"NÃO EXISTE",len(self.dictFont))
        (pix, width, height) = self.font.get_ch(ch)
        # print(width,height,foreground,background,''.join('{:02x}'.format(x) for x in bytes(pix)))

        foreground_bytes = foreground.to_bytes(2, 'big')
        background_bytes = background.to_bytes(2, 'big')

        count = width * height * 2
        # print("get_image(): alocating: %d bytes"%count,width,height,ch)
        image = bytearray(count)
        img_ptr = 0
        pix_ptr = 0
        bit = 0
        for y in range(height):
            # print()
            if bit != 0:
                bit = 0
                pix_ptr += 1
            for x in range(width):
                # print("x=%d y=%d img_ptr=%d pix_ptr=%d bit=%d"%(x,y,img_ptr,pix_ptr,bit))
                #                if img_ptr<count:
                # ptr=img_ptr+2*width*(height-1)-y*4*width
                ptr = -2 * x + (y + 1) * (width) * 2 - 2
                #                         print("ptr=",ptr)
                if (0x01 << bit) & pix[pix_ptr]:
                    image[ptr] = foreground_bytes[0]
                    image[ptr + 1] = foreground_bytes[1]
                    # print('#',end='')
                else:
                    image[ptr] = background_bytes[0]
                    image[ptr + 1] = background_bytes[1]
                    # print(" ",end='')
                img_ptr += 2
                bit += 1
                if bit >= 8:
                    bit = 0
                    pix_ptr += 1

        #            self.dictFont[ch]=[image,width,height]

        return (image, width, height)