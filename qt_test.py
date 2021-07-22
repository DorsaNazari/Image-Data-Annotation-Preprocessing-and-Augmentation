import os
import glob
import sys
from typing import Counter
from PyQt5.QtGui import QColor, QFont, QStandardItemModel, QStandardItem, QIcon, QPixmap
import numpy as np
from PyQt5.QtWidgets import (
    QFileDialog,
    QGraphicsDropShadowEffect,
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QDialog,
    QTreeWidgetItem,
    QTreeView,
)
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.Qt import QStandardItemModel
import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from time import sleep
from image import Image
from funcs import allImagesInThisDirectory, allImagesInThisDirectory2, eazyCrop, label
import cv2
import random


my_form_SplashScreen = uic.loadUiType(os.path.join(os.getcwd(), "first.ui"))[0]
my_form_main = uic.loadUiType(os.path.join(os.getcwd(), "main.ui"))[0]
my_form_flip = uic.loadUiType(os.path.join(os.getcwd(), "flipWindow.ui"))[0]
my_form_brightness = uic.loadUiType(os.path.join(os.getcwd(), "brightnessWindow.ui"))[0]
my_form_rotation = uic.loadUiType(os.path.join(os.getcwd(), "rotationWindow.ui"))[0]
my_form_noise = uic.loadUiType(os.path.join(os.getcwd(), "noiseWindow.ui"))[0]
my_form_blurring = uic.loadUiType(os.path.join(os.getcwd(), "blurringWindow.ui"))[0]
my_form_crop = uic.loadUiType(os.path.join(os.getcwd(), "cropWindow.ui"))[0]
my_form_upload = uic.loadUiType(os.path.join(os.getcwd(), "uploadWindow.ui"))[0]
my_form_tag = uic.loadUiType(os.path.join(os.getcwd(), "taggingWindow.ui"))[0]
my_form_split = uic.loadUiType(os.path.join(os.getcwd(), "splitWindow.ui"))[0]
my_form_filtering = uic.loadUiType(os.path.join(os.getcwd(), "filteringWindow.ui"))[0]
my_form_resize = uic.loadUiType(os.path.join(os.getcwd(), "resizeWindow.ui"))[0]


##global
Counter = 0
# Uploading
class UploadWindow(QMainWindow, my_form_upload):
    _count = 0

    def __init__(self):
        super(UploadWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Upload")
        self.browse.clicked.connect(self.browseImages)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_4.clicked.connect(self.exit)

    def exit(self):
        self.close()

    def browseImages(self):
        imagePath = QFileDialog.getExistingDirectory(self, "Select file")
        list_of_images_directory = allImagesInThisDirectory2(imagePath)
        l = len(list_of_images_directory)
        if l == 0:
            self.label.setText("There is no image here!")
        else:
            for i in range(l):
                UploadWindow._count += 1
                name = str(UploadWindow._count)
                pixmap = QPixmap(list_of_images_directory[i])
                pixmap = pixmap.scaled(600, 450)
                pixmap.save(".\images\image" + name + ".jpg")
            selectedImage = QPixmap(list_of_images_directory[0])
            selectedImage = selectedImage.scaled(600, 450)
            selectedImage.save("2.jpg")
            selectedImage = selectedImage.scaled(240, 180)
            selectedImage.save("1.jpeg")
            selectedImage.save("1.jpg")
            self.label.setText("<strong>Successfully Uploaded!</strong>")


## flip window
class FlipWindow(QMainWindow, my_form_flip):
    def __init__(self):
        super(FlipWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Flip')
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.imagename = "1"
        self.imagename = str(np.clip(int(self.imagename), None, UploadWindow._count - 1) + 1)
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(550,350)
        self.label_original_image.setPixmap(pixmap)
        self.label_original_image.setAlignment(QtCore.Qt.AlignCenter)

        # self.checkBox_h.stateChanged.connect(self.state_changed)
        # self.checkBox_v.stateChanged.connect(self.state_changed)
        self.pushButton.clicked.connect(self.state_changed )
        self.pushButton_4.clicked.connect(self.exit)

    def exit(self):
        self.close()

    def state_changed(self, int):

        src = cv2.imread("1.jpg")
        imgObject = Image("./images/image" + self.imagename + ".jpg")
        image = cv2.resize(imgObject.img, (550, 350))
        cv2.imwrite("my.jpg", image)
        src = cv2.imread("my.jpg")

        if not(self.checkBox_h.isChecked() & self.checkBox_v.isChecked()):
            self.label_fliped_image.setText(" ")
        if self.checkBox_v.isChecked():
            img = cv2.flip(src, 0)
            cv2.imwrite("my.png", img)
            pixmap = QtGui.QPixmap('my.png')
            self.label_fliped_image.setPixmap(pixmap)
            self.label_fliped_image.show()
        if self.checkBox_h.isChecked():
            img = cv2.flip(src, 1)
            cv2.imwrite("my.png", img)
            pixmap = QtGui.QPixmap('my.png')
            self.label_fliped_image.setPixmap(pixmap)
            self.label_fliped_image.show()
        if self.checkBox_h.isChecked() & self.checkBox_v.isChecked():
            img = cv2.flip(src, -1)
            cv2.imwrite("my.png", img)
            pixmap = QtGui.QPixmap('my.png')
            self.label_fliped_image.setPixmap(pixmap)
            self.label_fliped_image.show()


## resize window
class ResizeWindow(QMainWindow, my_form_resize):
    def __init__(self):
        super(ResizeWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Resize')
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.imagename = "1"
        self.imagename = str(np.clip(int(self.imagename), None, UploadWindow._count - 1) + 1)
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(550,350)
        self.label_original_image.setPixmap(pixmap)
        self.label_original_image.setAlignment(QtCore.Qt.AlignCenter)

        self.pushButton.clicked.connect(self.state_changed )
        self.pushButton_4.clicked.connect(self.exit)

    def exit(self):
        self.close()

    def state_changed(self, int):
        h = np.int64(float(self.height.text()))
        w = np.int64(float(self.width.text()))

        # resize image
        imgObject = Image("./images/image" + self.imagename + ".jpg")
        image = cv2.resize(imgObject.img, (550, 350))

        im=cv2.imwrite("my.jpg", image)
        src = cv2.imread("my.jpg")
        height = np.int(src.shape[0] * h / 100)
        width = np.int(src.shape[1] * w / 100)
        dim = (width, height)
  
        img = cv2.resize(src, dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite("my.png", img)
        pixmap = QtGui.QPixmap('my.png')
        self.label_resized_image.setPixmap(pixmap)
        self.label_resized_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_resized_image.show()


# brightness window
class BrightnessWindow(QMainWindow, my_form_brightness):
    def __init__(self):
        super(BrightnessWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Brightness")
        self.horizontalSlider.valueChanged.connect(self.state_changed)
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_5.clicked.connect(self.applyToAll)

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        for img in my_list:
            ans = img.adjustBrightness(self.int / 100)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)

    def exit(self):
        self.close()

    def state_changed(self, int):
        self.int = int
        imgObject = Image("2.jpg")
        img = imgObject.adjustBrightness(int / 100)
        cv2.imwrite("ui.jpg", img)
        pixmap = QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)


# rotation window
class RotationWindow(QMainWindow, my_form_rotation):
    def __init__(self):
        super(RotationWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("rotation")
        self.horizontalSlider.valueChanged.connect(self.state_changed)
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_7.clicked.connect(self.exit)
        self.pushButton_8.clicked.connect(self.applyToAll)

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")

        for img in my_list:
            ans = img.rotate(-self.int)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)

    def exit(self):
        self.close()

    def state_changed(self, int):
        self.int = int
        imgObject = Image("2.jpg")
        img = imgObject.rotate(-int)
        cv2.imwrite("ui.jpg", img)
        pixmap = QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)


# noise window
class NoiseWindow(QMainWindow, my_form_noise):
    def __init__(self):
        super(NoiseWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("noise")
        self.mode = None
        self.horizontalSlider.hide()
        self.horizontalSlider.valueChanged.connect(self.state_changed)
        self.pushButton.clicked.connect(self.gauss)
        self.pushButton_2.clicked.connect(self.speckle)
        self.pushButton_3.clicked.connect(self.poisson)
        self.pushButton_4.clicked.connect(self.salt)
        self.pushButton_5.clicked.connect(self.pepper)
        self.pushButton_6.clicked.connect(self.sp)
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_7.clicked.connect(self.exit)
        self.pushButton_8.clicked.connect(self.applyToAll)

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")

        for img in my_list:
            ans = img.addnoise(self.mode, self.int / 100)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)

    def exit(self):
        self.close()

    def gauss(self):
        self.mode = "gaussian"
        self.horizontalSlider.show()

    def speckle(self):
        self.mode = "speckle"
        self.horizontalSlider.show()

    def poisson(self):
        self.mode = "poisson"
        self.horizontalSlider.hide()
        imgObject = Image("2.jpg")
        img = imgObject.addnoise(self.mode)
        cv2.imwrite("ui.jpg", img)
        pixmap = QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)

    def salt(self):
        self.mode = "salt"
        self.horizontalSlider.show()

    def pepper(self):
        self.mode = "pepper"
        self.horizontalSlider.show()

    def sp(self):
        self.mode = "s&p"
        self.horizontalSlider.show()

    def state_changed(self, int):
        imgObject = Image("2.jpg")
        self.int = int
        img = imgObject.addnoise(self.mode, int / 100)
        cv2.imwrite("ui.jpg", img)
        pixmap = QtGui.QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)


# blurring window
class BlurringWindow(QMainWindow, my_form_blurring):
    def __init__(self):
        super(BlurringWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("blurring")
        self.mode = None
        self.horizontalSlider.hide()

        self.horizontalSlider.valueChanged.connect(self.state_changed)
        self.pushButton.clicked.connect(self.gauss)
        self.pushButton_2.clicked.connect(self.median)
        self.pushButton_3.clicked.connect(self.bilateral)
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_5.clicked.connect(self.applyToAll)

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def applyToAll(self):
        my_list = allImagesInThisDirectory("./images")
        if self.int % 2 == 0:
            self.int += 1
        for img in my_list:
            if self.mode == "g":
                ans = cv2.GaussianBlur(img.img, (self.int, self.int), 0)
            elif self.mode == "m":
                ans = cv2.medianBlur(img.img, self.int)
            elif self.mode == "b":
                ans = cv2.bilateralFilter(img.img, self.int, 75, 75)
            UploadWindow._count += 1
            cv2.imwrite(".\images\image" + str(UploadWindow._count) + ".jpg", ans)

    def gauss(self):
        self.mode = "g"
        self.horizontalSlider.show()

    def median(self):
        self.mode = "m"
        self.horizontalSlider.show()

    def bilateral(self):
        self.mode = "b"
        self.horizontalSlider.show()

    def exit(self):
        self.close()

    def state_changed(self, int):
        self.int = int
        imgObject = Image("2.jpg")
        if int % 2 == 0:
            int += 1
        if self.mode == "g":
            ans = cv2.GaussianBlur(imgObject.img, (int, int), 0)
        elif self.mode == "m":
            ans = cv2.medianBlur(imgObject.img, int)
        elif self.mode == "b":
            ans = cv2.bilateralFilter(imgObject.img, int, 75, 75)
        cv2.imwrite("ui.jpg", ans)
        pixmap = QPixmap("ui.jpg")
        self.label.setPixmap(pixmap)


# crop window
class CropWindow(QMainWindow, my_form_crop):
    def __init__(self):
        super(CropWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("crop")
        self.ref_point = []
        self.pushButton_6.clicked.connect(self.next)
        self.pushButton_3.clicked.connect(self.prev)
        self.pushButton.clicked.connect(self.apply)
        self.imagename = "1"
        self.pushButton_4.clicked.connect(self.exit)

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def prev(self):
        self.imagename = str(np.clip(int(self.imagename), 2, None) - 1)
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        self.label.setPixmap(pixmap)
        if os.path.isfile("./cropped/croppedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./cropped/croppedimage" + self.imagename + ".jpg")
        self.label_2.setPixmap(pixmap)

    def next(self):
        self.imagename = str(
            np.clip(int(self.imagename), None, UploadWindow._count - 1) + 1
        )
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        self.label.setPixmap(pixmap)
        if os.path.isfile("./cropped/croppedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./cropped/croppedimage" + self.imagename + ".jpg")
        self.label_2.setPixmap(pixmap)

    def apply(self):
        image = cv2.imread("ui.jpg")
        cv2.imwrite("./cropped/croppedimage" + self.imagename + ".jpg", image)

    def mousePressEvent(self, event):
        self.originQPoint = [event.x(), event.y()]
        self.ref_point.append(self.originQPoint)
        self.originQPoint = event.pos()
        self.currentQRubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self
        )
        self.currentQRubberBand.setGeometry(
            QtCore.QRect(self.originQPoint, QtCore.QSize())
        )
        self.currentQRubberBand.show()

    def mouseMoveEvent(self, event):
        self.currentQRubberBand.setGeometry(
            QtCore.QRect(self.originQPoint, event.pos()).normalized()
        )

    def mouseReleaseEvent(self, event):
        self.endQPoint = [event.x(), event.y()]
        self.ref_point.append(self.endQPoint)
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        if (
            self.ref_point[0][0] == self.ref_point[1][0]
            or self.ref_point[0][1] == self.ref_point[1][1]
        ):
            self.ref_point.clear()
            return
        imgObject = Image("./images/image" + self.imagename + ".jpg")
        image = cv2.resize(imgObject.img, (600, 450))
        if self.ref_point[0][1] < 280:
            self.ref_point[0][1] = 280
        if self.ref_point[1][1] < 280:
            self.ref_point[1][1] = 280
        if self.ref_point[1][1] > 730:
            self.ref_point[1][1] = 730
        if self.ref_point[0][1] > 730:
            self.ref_point[0][1] = 730
        if self.ref_point[0][0] < 30:
            self.ref_point[0][0] = 30
        if self.ref_point[1][0] < 30:
            self.ref_point[1][0] = 30
        if self.ref_point[0][0] > 630:
            self.ref_point[0][0] = 630
        if self.ref_point[1][0] > 630:
            self.ref_point[1][0] = 630
        croped = image[
            min(self.ref_point[0][1], self.ref_point[1][1])
            - 280 : max(self.ref_point[0][1], self.ref_point[1][1])
            - 280,
            min(self.ref_point[0][0], self.ref_point[1][0])
            - 30 : max(self.ref_point[0][0], self.ref_point[1][0])
            - 30,
        ]
        cv2.imwrite("ui.jpg", croped)
        pixmap = QPixmap("ui.jpg")
        self.label_2.setPixmap(pixmap)
        self.ref_point.clear()

    def exit(self):
        self.close()


# tag window
class TaggingWindow(QMainWindow, my_form_tag):
    def __init__(self):
        super(TaggingWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Tagging")
        self.ref_point = [None, None]
        self.pushButton_4.clicked.connect(self.exit)
        self.pushButton_6.clicked.connect(self.next)
        self.pushButton_3.clicked.connect(self.prev)
        self.pushButton.clicked.connect(self.apply)
        self.imagename = "1"
        self.totalTexts = []
        self.lineEdit.hide()
        self.lineEdit.returnPressed.connect(self.tag)
        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def prev(self):
        self.imagename = str(np.clip(int(self.imagename), 2, None) - 1)
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        self.label.setPixmap(pixmap)
        if os.path.isfile("./tagged/taggedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./tagged/taggedimage" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label_2.setPixmap(pixmap)
        self.lineEdit.hide()

    def next(self):
        self.lineEdit.hide()
        self.imagename = str(
            np.clip(int(self.imagename), None, UploadWindow._count - 1) + 1
        )
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        self.label.setPixmap(pixmap)
        if os.path.isfile("./tagged/taggedimage" + self.imagename + ".jpg"):
            pixmap = QPixmap("./tagged/taggedimage" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label_2.setPixmap(pixmap)

    def apply(self):
        image = cv2.imread("ui.jpg")
        cv2.imwrite("./tagged/taggedimage" + self.imagename + ".jpg", image)
        file1 = open("./tagged/ref_pointsOfimage" + self.imagename + ".txt", "a")
        file1.write(str(self.ref_point) + "\t" + self.totalTexts[-1] + "\n")
        file1.close()

    def tag(self):
        self.totalTexts.append(self.lineEdit.text())
        imageObject = Image("ui.jpg")
        image = imageObject.img
        self.x += 1
        self.y += 15
        cv2.putText(
            image,
            self.totalTexts[-1],
            (self.x, self.y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 120),
            2,
        )
        cv2.imwrite("ui.jpg", image)
        pixmap = QPixmap("ui.jpg")
        self.label_2.setPixmap(pixmap)
        self.lineEdit.clear()
        self.lineEdit.hide()

    def mousePressEvent(self, event):
        self.originQPoint = [event.x(), event.y()]
        self.ref_point[0] = self.originQPoint
        self.originQPoint = event.pos()
        self.currentQRubberBand = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self
        )
        self.currentQRubberBand.setGeometry(
            QtCore.QRect(self.originQPoint, QtCore.QSize())
        )
        self.currentQRubberBand.show()

    def mouseMoveEvent(self, event):
        self.currentQRubberBand.setGeometry(
            QtCore.QRect(self.originQPoint, event.pos()).normalized()
        )

    def mouseReleaseEvent(self, event):
        self.endQPoint = [event.x(), event.y()]
        self.ref_point[1] = self.endQPoint
        self.currentQRubberBand.hide()
        currentQRect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()
        if (
            self.ref_point[0][0] == self.ref_point[1][0]
            or self.ref_point[0][1] == self.ref_point[1][1]
        ):
            return
        imgObject = Image("./images/image" + self.imagename + ".jpg")
        if os.path.isfile("./tagged/taggedimage" + self.imagename + ".jpg"):
            imgObject = Image("./tagged/taggedimage" + self.imagename + ".jpg")

        image = cv2.resize(imgObject.img, (600, 450))
        pixmap = QPixmap("./images/image" + self.imagename + ".jpg")
        pixmap = pixmap.scaled(600, 450)
        self.label.setPixmap(pixmap)
        if self.ref_point[0][1] < 280:
            self.ref_point[0][1] = 280
        if self.ref_point[1][1] < 280:
            self.ref_point[1][1] = 280
        if self.ref_point[1][1] > 730:
            self.ref_point[1][1] = 730
        if self.ref_point[0][1] > 730:
            self.ref_point[0][1] = 730
        if self.ref_point[0][0] < 30:
            self.ref_point[0][0] = 30
        if self.ref_point[1][0] < 30:
            self.ref_point[1][0] = 30
        if self.ref_point[0][0] > 630:
            self.ref_point[0][0] = 630
        if self.ref_point[1][0] > 630:
            self.ref_point[1][0] = 630
        self.x = min(self.ref_point[0][0], self.ref_point[1][0]) - 30
        x2 = max(self.ref_point[0][0], self.ref_point[1][0]) - 30
        self.y = min(self.ref_point[0][1], self.ref_point[1][1]) - 280
        y2 = max(self.ref_point[0][1], self.ref_point[1][1]) - 280

        image = cv2.rectangle(
            image,
            (self.x, self.y),
            (x2, y2),
            (255, 0, 255),
            1,
        )
        self.lineEdit.show()
        cv2.imwrite("ui.jpg", image)
        pixmap = QPixmap("ui.jpg")
        self.label_2.setPixmap(pixmap)

    def exit(self):
        self.close()


# filtering
class FilteringWindow(QMainWindow, my_form_filtering):
    def __init__(self):
        super(FilteringWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("filtering")

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.pushButton.clicked.connect(self.apply_invert)
        self.pushButton_2.clicked.connect(self.apply_sepia)
        self.pushButton_3.clicked.connect(self.destroy)
        self.pushButton_4.clicked.connect(self.Morphological)
        self.pushButton_5.clicked.connect(self.openning)
        self.pushButton_6.clicked.connect(self.grayScale)
        self.pushButton_7.clicked.connect(self.denoise)
        self.pushButton_8.clicked.connect(self.exit)

    def exit(self):
        self.close()

    def apply_invert(self):
        imgObject = cv2.imread("2.jpg")
        cv2.imwrite("ui.jpg", cv2.bitwise_not(imgObject))
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def grayScale(self):
        imgObject = cv2.imread("2.jpg")
        gray = imgObject.copy()
        gray = gray.astype(np.float)
        gray[:, :, 0] = gray[:, :, 1] = gray[:, :, 2] = 1.5 * np.mean(imgObject, 2)
        gray[gray > 255] = 255
        gray = gray.astype(np.uint8)
        cv2.imwrite("ui.jpg", cv2.bitwise_not(gray))
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def apply_sepia(self):
        img = cv2.imread("2.jpg")
        img = np.array(img, dtype=np.float64)  # converting to float to prevent loss
        img = cv2.transform(
            img,
            np.matrix(
                [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.869]]
            ),
        )  # multipying image with special sepia matrix
        img[np.where(img > 255)] = 255  # normalizing values greater than 255 to 255
        img = np.array(img, dtype=np.uint8)  # converting back to int
        cv2.imwrite("ui.jpg", cv2.bitwise_not(img))
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def destroy(self):
        img = cv2.imread("2.jpg")
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        lower_red = np.array([10, 10, 10])
        upper_red = np.array([240, 240, 240])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(img, img, mask=mask)
        cv2.imwrite("ui.jpg", res)
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def Morphological(self):
        img = cv2.imread("2.jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        cv2.imwrite("ui.jpg", gradient)
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def openning(self):
        img = cv2.imread("2.jpg", 0)
        kernel = np.ones((5, 5), np.uint8)
        openning = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        cv2.imwrite("ui.jpg", openning)
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)

    def denoise(self):
        imgObject = Image("2.jpg")
        img = imgObject.denoise()
        cv2.imwrite("ui.jpg", img)
        pixmap = QPixmap("ui.jpg")
        self.label_filtering.setPixmap(pixmap)


# Split
class SplitWindow(QMainWindow, my_form_split):
    def __init__(self):
        super(SplitWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Split")

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        imagePath = ".\images"
        list_of_images_directory = allImagesInThisDirectory2(imagePath)
        self.num =  len(list_of_images_directory)
        if self.num == 0:
            self.label_3.setText("You did not upload images!")
        self.label.setText(f"{self.num}")
        self.ch = 0
        self.Enter.clicked.connect(self.enter_pressed)
        self.OK_Button.clicked.connect(self.OK_pressed)
        self.pushButton_4.clicked.connect(self.exit)

    def exit(self):
        self.close()
        

    def enter_pressed(self):
        if self.lineEdit.text() != '':
            self.ch = 1
            pTrain = float(self.lineEdit.text())
            if pTrain>100 or pTrain<0 :
                self.label_3.setText("it is not percentage!")
            else:
                self.label_3.clear()
                self.train = int(pTrain * self.num /100)
                self.label_4.setText(f"The Split data number is :     {self.train} images for Train\n\t\t\t {self.num - self.train} images for Test\n\t\t\t  is it OK ?")
            
    
    def OK_pressed(self):
        if self.ch == 0:
            self.label_3.setText("First Press Enter!")
        else:
            self.Trainlist = random.sample(range(1,self.num), self.train)
            self.doSplit()
            self.close()


    def doSplit(self):
        list_of_images_directory = allImagesInThisDirectory2(".\images")
        j = k = 1
        for i in range(len(list_of_images_directory)):
            pixmap = QPixmap(list_of_images_directory[i])
            if i in self.Trainlist:
                pixmap.save(f".\splitData\Train\image{j}.jpg")
                j+=1
            else:
                pixmap.save(f".\splitData\Test\image{k}.jpg")
                k+=1
                
            
                





##making treeview pretty
class StandardItem(QStandardItem, my_form_main):
    def __init__(self, txt="", font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()
        fnt = QFont("Open Sans", font_size)
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        # self.setBackground(color_b)
        self.setFont(fnt)
        self.setText(txt)


## application
class MainWindow(QMainWindow, my_form_main):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        ##remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(700, 500)

        ##tree
        treeView = QTreeView()
        treeView.setHeaderHidden(True)
        treeView.setAnimated(True)
        treeView.setIndentation(100)
        # treeView.setGeometry(QRect(0, 0, 882, 346))
        treeView.setStyleSheet(
            (
                "QTreeView {    \n"
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
                ""
            )
        )
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        #########################################################
        source_images = StandardItem(
            "Source Images", 35, color=QColor(96, 100, 152), set_bold=True
        )
        upload = StandardItem("Upload", 25, color=QColor(254, 121, 199))
        source_images.appendRow(upload)

        annotate = StandardItem(
            "Annotate", 35, color=QColor(96, 100, 152), set_bold=True
        )
        tagging = StandardItem("Tagging", 25, color=QColor(254, 121, 199))
        annotate.appendRow(tagging)

        preprocessing = StandardItem(
            "Preprocessing", 35, color=QColor(96, 100, 152), set_bold=True
        )
        resize = StandardItem("Resize", 25, color=QColor(254, 121, 199))
        preprocessing.appendRow(resize)

        augmentation = StandardItem(
            "Augmentation", 35, color=QColor(96, 100, 152), set_bold=True
        )
        flip = StandardItem("Flip", 25, color=QColor(254, 121, 199))
        crop = StandardItem("Crop", 25, color=QColor(254, 121, 199))
        rotation = StandardItem("Rotation", 25, color=QColor(254, 121, 199))
        brightness = StandardItem("Brightness", 25, color=QColor(254, 121, 199))
        noise = StandardItem("Noise", 25, color=QColor(254, 121, 199))
        blurring = StandardItem("Blurring", 25, color=QColor(254, 121, 199))
        filtering = StandardItem("Filtering", 25, color=QColor(254, 121, 199))
        augmentation.appendRow(flip)
        augmentation.appendRow(crop)
        augmentation.appendRow(rotation)
        augmentation.appendRow(brightness)
        augmentation.appendRow(noise)
        augmentation.appendRow(blurring)
        augmentation.appendRow(filtering)

        tran_test_split = StandardItem(
            "Train/Test Split", 35, color=QColor(96, 100, 152), set_bold=True
        )
        split = StandardItem("Split", 25, color=QColor(254, 121, 199))
        tran_test_split.appendRow(split)

        generate = StandardItem(
            "Generate", 35, color=QColor(96, 100, 152), set_bold=True
        )
        ready = StandardItem("Ready", 25, color=QColor(254, 121, 199))
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

    def action(self, val):
        if val.data() == "Upload":
            print(val.data())
            self.flip = UploadWindow()
            self.flip.show()
        if val.data() == "Flip":
            print(val.data())
            self.flip = FlipWindow()
            self.flip.show()
        if val.data() == "Resize":
            print(val.data())
            self.flip = ResizeWindow()
            self.flip.show()
        if val.data() == "Brightness":
            print(val.data())
            self.brightness = BrightnessWindow()
            self.brightness.show()
        if val.data() == "Rotation":
            print(val.data())
            self.rotation = RotationWindow()
            self.rotation.show()
        if val.data() == "Noise":
            print(val.data())
            self.noise = NoiseWindow()
            self.noise.show()
        if val.data() == "Blurring":
            print(val.data())
            self.blurring = BlurringWindow()
            self.blurring.show()
        if val.data() == "Crop":
            print(val.data())
            self.crop = CropWindow()
            self.crop.show()
        if val.data() == "Tagging":
            print(val.data())
            self.tag = TaggingWindow()
            self.tag.show()
        if val.data() == "Filtering":
            print(val.data())
            self.filtering = FilteringWindow()
            self.filtering.show()
        if val.data() == "Split":
            print(val.data())
            self.split = SplitWindow()
            self.split.show()


## splash screen
class SplashScreen(QMainWindow, my_form_SplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.setupUi(self)
        ##remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ##drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)
        ##Qtimer ==> start
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        ##timer in ms
        self.timer.start(35)
        # change description
        self.label_description.setText("<strong>WELCOME</strong> TO OUR APPLICATION")
        QtCore.QTimer.singleShot(
            3000,
            lambda: self.label_description.setText(" PREPROCESSING AND AUGMENTATION "),
        )

    def progress(self):
        global Counter
        # set value to progress bar
        self.progressBar.setValue(Counter)
        # close splash screen and open app
        if Counter > 100:
            # stop timer
            self.timer.stop()
            # show main window
            self.main = MainWindow()
            self.main.show()
            # close splash screen
            self.close()
        # increase counter
        Counter += 1


files = glob.glob("./images/*") + glob.glob("./cropped/*") + glob.glob("./tagged/*")
for f in files:
    os.remove(f)

app = QApplication([])
w = SplashScreen()
w.show()
sys.exit(app.exec_())


