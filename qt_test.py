import os
import sys
from typing import Counter
from PyQt5.QtGui import QColor, QFont, QStandardItemModel ,QStandardItem 
import numpy as np
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QApplication, QVBoxLayout,QDialog,QTreeWidgetItem,QTreeView
from PyQt5 import uic, QtCore,QtWidgets,QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.Qt import QStandardItemModel
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from time import sleep
from image import Image
from funcs import allImagesInThisDirectory, eazyCrop, label
import cv2



my_form_SplashScreen = uic.loadUiType(os.path.join(os.getcwd(), "first.ui"))[0]
my_form_main = uic.loadUiType(os.path.join(os.getcwd(), "main.ui"))[0]
my_form_flip = uic.loadUiType(os.path.join(os.getcwd(), "flipWindow.ui"))[0]


##global
Counter = 0
##flip window
class FlipWindow(QMainWindow, my_form_flip):
    def __init__(self):
        super(FlipWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Flip')
        # self.resize(900,700)

        label = self.label_original_image
        pixmap = QtGui.QPixmap("1.jpg")
        label.setPixmap(pixmap)
        label.show()

        self.checkBox_h.stateChanged.connect(self.state_changed)
        self.checkBox_v.stateChanged.connect(self.state_changed)

    def state_changed(self, int):
        if self.checkBox_h.isChecked():
            print(int)
        if self.checkBox_v.isChecked():
            print(int)


##making treeview pretty
class StandardItem(QStandardItem,my_form_main):
    def __init__ (self,txt = "" ,font_size =12 , set_bold = False,color= QColor(0,0,0)):
        super().__init__()
        fnt = QFont('Open Sans',font_size)
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        # self.setBackground(color_b)
        self.setFont(fnt)
        self.setText(txt)

## application
class MainWindow(QMainWindow, my_form_main):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        ##remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(700,500)        

        ##tree
        treeView = QTreeView()
        treeView.setHeaderHidden(True)
        treeView.setAnimated(True)
        treeView.setIndentation(100)
        # treeView.setGeometry(QRect(0, 0, 882, 346))
        treeView.setStyleSheet(("QTreeView {    \n"
    "    background-color: rgb(39, 44, 54);\n"
    "    padding: 10px;\n"
    "    border-radius: 15px;\n"
    "    gridline-color: rgb(44, 49, 60);\n"
    "    border-bottom: 1px solid rgb(44, 49, 60);\n"
    "}\n"
    "QTreeView::item{\n"
    "    border-color: rgb(44, 49, 60);\n"
    "    padding-left: 5px;\n"
    "    padding-right: 5px;\n"
    "    gridline-color: rgb(44, 49, 60);\n"
    "}\n"
    "QTreeView::item:selected{\n"
    "    background-color: rgb(85, 170, 255);\n"
    "}\n"
    "QScrollBar:horizontal {\n"
    "    border: none;\n"
    "    background: rgb(52, 59, 72);\n"
    "    height: 14px;\n"
    "    margin: 0px 21px 0 21px;\n"
    "    border-radius: 0px;\n"
    "}\n"
    " QScrollBar:vertical {\n"
    "    border: none;\n"
    "    background: rgb(52, 59, 72);\n"
    "    width: 14px;\n"
    "    margin: 21px 0 21px 0;\n"
    "    border-radius: 0px;\n"
    " }\n"
    "QHeaderView::section{\n"
    "    Background-color: rgb(39, 44, 54);\n"
    "    max-width: 30px;\n"
    "    border: 1px solid rgb(44, 49, 60);\n"
    "    border-style: none;\n"
    "    border-bottom: 1px solid rgb(44, 49, 60);\n"
    "    border-right: 1px solid rgb(44, 49, 60);\n"
    "}\n"
    "QTreeView::horizontalHeader {    \n"
    "    background-color: rgb(81, 255, 0);\n"
    "}\n"
    "QHeaderView::section:horizontal\n"
    "{\n"
    "    border: 1px solid rgb(32, 34, 42);\n"
    "    background-color: rgb(27, 29, 35);\n"
    "    padding: 3px;\n"
    "    border-top-left-radius: 20px;\n"
    "    border-top-right-radius: 20px;\n"
    "}\n"
    "QHeaderView::section:vertical\n"
    "{\n"
    "    border: 1px solid rgb(44, 49, 60);\n"
    "}\n"
    "QTreeView QTreeViewCornerButton::section\n"
    "{\n"
    "background-color:red\n"
    "}\n"
    ""))
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
 #########################################################
        source_images = StandardItem('Source Images',35,color=QColor(96,100,152),set_bold=True)
        upload = StandardItem('Upload',25,color=QColor(254,121,199))
        source_images.appendRow(upload)

        annotate = StandardItem('Annotate',35,color=QColor(96,100,152),set_bold=True)
        tagging = StandardItem('Tagging',25,color=QColor(254,121,199))
        annotate.appendRow(tagging)

        preprocessing = StandardItem('Preprocessing',35,color=QColor(96,100,152),set_bold=True)
        resize = StandardItem('Resize',25,color=QColor(254,121,199))
        grayscale = StandardItem('Grayscale',25,color=QColor(254,121,199))
        preprocessing.appendRow(resize)
        preprocessing.appendRow(grayscale)

        augmentation = StandardItem('Augmentation',35,color=QColor(96,100,152),set_bold=True)
        flip = StandardItem('Flip',25,color=QColor(254,121,199))
        crop = StandardItem('Crop',25,color=QColor(254,121,199))
        rotation = StandardItem('Rotation',25,color=QColor(254,121,199))
        brightness = StandardItem('Brightness',25,color=QColor(254,121,199))
        noise = StandardItem('Noise',25,color=QColor(254,121,199))
        blurring = StandardItem('Blurring',25,color=QColor(254,121,199))
        filtering = StandardItem('Filtering',25,color=QColor(254,121,199))
        augmentation.appendRow(flip)
        augmentation.appendRow(crop)
        augmentation.appendRow(rotation)
        augmentation.appendRow(brightness)
        augmentation.appendRow(noise)
        augmentation.appendRow(blurring)
        augmentation.appendRow(filtering)

        tran_test_split = StandardItem('Train/Test Split',35,color=QColor(96,100,152),set_bold=True)
        split = StandardItem('Split',25,color=QColor(254,121,199))
        tran_test_split.appendRow(split)

        generate = StandardItem('Generate',35,color=QColor(96,100,152),set_bold=True)
        ready = StandardItem('Ready',25,color=QColor(254,121,199))
        generate.appendRow(ready)

        rootNode.appendRow(source_images)
        rootNode.appendRow(annotate)
        rootNode.appendRow(preprocessing)
        rootNode.appendRow(augmentation)
        rootNode.appendRow(tran_test_split)
        rootNode.appendRow(generate)


        treeView.setModel(treeModel)
        treeView.expandAll()

        treeView.doubleClicked.connect(self.action)

        self.setCentralWidget(treeView)
    
    def action (self,val):
        # imgObject = Image("test.jpeg")
        if val.data() == "Flip":
            print(val.data())
            self.flip = FlipWindow()
            self.flip.show()
            # img = cv2.flip(imgObject.img, 1)
            # cv2.imshow("original", img)
            # cv2.waitKey()
            # cv2.destroyAllWindows()


            
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









    #     self.printtree()

    # def printtree(self):
    #     self.treeWidget.setColumnCount(3)
    #     a =QTreeWidgetItem(["preprocessing"])
    #     self.treeWidget.addTopLevelItem(a)
