import os
import sys
from typing import Counter
from PyQt5.QtGui import QColor 
import numpy as np
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QApplication, QVBoxLayout
from PyQt5 import uic, QtCore
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from time import sleep
import plot_thread as pt


my_form_SplashScreen = uic.loadUiType(os.path.join(os.getcwd(), "first.ui"))[0]
my_form_main = uic.loadUiType(os.path.join(os.getcwd(), "main.ui"))[0]

##global
Counter = 0

## application
class MainWindow(QMainWindow, my_form_main):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)

## splash screen
class SplashScreen(QMainWindow, my_form_SplashScreen):
    def __init__(self):
        super(SplashScreen,self).__init__()
        self.setupUi(self)
        ##remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ##drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,60))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)
        ##Qtimer ==> start
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        ##timer in ms
        self.timer.start(35)
        #change description
        self.label_description.setText("<strong>WELCOME</strong> TO OUR APPLICATION")
        QtCore.QTimer.singleShot(3000, lambda:self.label_description.setText(" PREPROCESSING AND AUGMENTATION "))

    def progress(self):
        global Counter
        # set value to progress bar
        self.progressBar.setValue(Counter)
        #close splash screen and open app
        if Counter > 100 :
            #stop timer
            self.timer.stop()
            #show main window
            self.main = MainWindow()
            self.main.show()
            #close splash screen
            self.close()
        # increase counter
        Counter += 1 


app = QApplication([])
w = SplashScreen()
w.show()
sys.exit(app.exec_())
print("hello qt :)")




















#     self.fig = Figure()
#     self.ax = self.fig.add_subplot(111)
#     # frame_on = False
#     self.canvas = FigureCanvas(self.fig)
#     self.navi = NavigationToolbar(self.canvas, self)

#     l = QVBoxLayout(self.matplotlib_widget)
#     l.addWidget(self.navi)
#     l.addWidget(self.canvas)

#     x = np.linspace(0, 6* np.pi, 1000)
#     self.line1, = self.ax.plot(x, np.cos(x), 'g',lw=3)
#     self.ax.text(np.pi,.5,r"$\sin(x)$",fontsize =20)

#     self.thread = None

#     #events
#     self.ok_pushButton.clicked.connect(self.ok_callback)
#     self.rand_lineEdit.textChanged.connect(self.func)

# def ok_callback(self):
#     if self.thread:
#         return
#     r = np.random.random()
#     self.rand_lineEdit.setText(f"num is: {r:.03f}")
#     print("hello world!! :))")
#     self.thread = pt.plot_thread(self, r)
#     self.thread.update_trigger.connect(self.update_plot)
#     self.thread.stop_trigger.connect(self.stop)
#     self.thread.start()
#     self.ok_pushButton.setEnabled(False)
    
# def update_plot(self, x, y):
#     self.line1.set_data(x, y)
#     self.fig.canvas.draw()

# def func(self):
#     print("test")

# def stop(self):
#     self.thread = None
#     self.rand_lineEdit.setText("STOP")
#     self.ok_pushButton.setEnabled(True)