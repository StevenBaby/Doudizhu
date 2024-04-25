# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1223, 861)
        font = QFont()
        font.setFamilies([u"DengXian"])
        font.setPointSize(20)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.card_frame = QFrame(self.centralwidget)
        self.card_frame.setObjectName(u"card_frame")
        self.card_frame.setMinimumSize(QSize(600, 800))
        font1 = QFont()
        font1.setFamilies([u"DengXian"])
        font1.setPointSize(16)
        self.card_frame.setFont(font1)
        self.card_frame.setFrameShape(QFrame.StyledPanel)
        self.card_frame.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.card_frame)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(300, 300))
        self.frame_2.setMaximumSize(QSize(300, 16777215))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Sunken)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.startButton = QPushButton(self.frame_2)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setMinimumSize(QSize(0, 80))

        self.verticalLayout.addWidget(self.startButton)

        self.showButton = QPushButton(self.frame_2)
        self.showButton.setObjectName(u"showButton")
        self.showButton.setMinimumSize(QSize(100, 80))

        self.verticalLayout.addWidget(self.showButton)

        self.hintButton = QPushButton(self.frame_2)
        self.hintButton.setObjectName(u"hintButton")
        self.hintButton.setMinimumSize(QSize(0, 80))

        self.verticalLayout.addWidget(self.hintButton)


        self.horizontalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1223, 35))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u6e38\u620f", None))
        self.showButton.setText(QCoreApplication.translate("MainWindow", u"\u51fa\u724c", None))
        self.hintButton.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u793a", None))
    # retranslateUi

