# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(930, 852)
        font = QFont()
        font.setFamilies([u"DengXian"])
        font.setPointSize(20)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.down_mark_frame = QFrame(self.centralwidget)
        self.down_mark_frame.setObjectName(u"down_mark_frame")
        self.down_mark_frame.setMinimumSize(QSize(300, 0))
        self.down_mark_frame.setMaximumSize(QSize(800, 60))
        font1 = QFont()
        font1.setFamilies([u"DengXian"])
        font1.setPointSize(16)
        self.down_mark_frame.setFont(font1)
        self.down_mark_frame.setFrameShape(QFrame.NoFrame)
        self.down_mark_frame.setFrameShadow(QFrame.Sunken)
        self.down_mark_layout = QHBoxLayout(self.down_mark_frame)
        self.down_mark_layout.setObjectName(u"down_mark_layout")
        self.down_mark_layout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.down_mark_frame, 0, 0, 1, 1)

        self.all_mark_frame = QFrame(self.centralwidget)
        self.all_mark_frame.setObjectName(u"all_mark_frame")
        self.all_mark_frame.setMinimumSize(QSize(300, 0))
        self.all_mark_frame.setMaximumSize(QSize(800, 60))
        self.all_mark_frame.setFont(font1)
        self.all_mark_frame.setFrameShape(QFrame.NoFrame)
        self.all_mark_frame.setFrameShadow(QFrame.Sunken)
        self.all_mark_layout = QHBoxLayout(self.all_mark_frame)
        self.all_mark_layout.setObjectName(u"all_mark_layout")
        self.all_mark_layout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.all_mark_frame, 0, 1, 1, 1)

        self.card_frame_11 = QFrame(self.centralwidget)
        self.card_frame_11.setObjectName(u"card_frame_11")
        self.card_frame_11.setMinimumSize(QSize(300, 0))
        self.card_frame_11.setFont(font1)
        self.card_frame_11.setFrameShape(QFrame.StyledPanel)
        self.card_frame_11.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.card_frame_11, 0, 2, 1, 1)

        self.down_frame = QFrame(self.centralwidget)
        self.down_frame.setObjectName(u"down_frame")
        self.down_frame.setMinimumSize(QSize(300, 100))
        self.down_frame.setFont(font1)
        self.down_frame.setFrameShape(QFrame.StyledPanel)
        self.down_frame.setFrameShadow(QFrame.Sunken)
        self.down_layout = QHBoxLayout(self.down_frame)
        self.down_layout.setSpacing(0)
        self.down_layout.setObjectName(u"down_layout")
        self.down_layout.setContentsMargins(9, 9, 9, 9)

        self.gridLayout.addWidget(self.down_frame, 1, 0, 1, 1)

        self.down_show_frame = QFrame(self.centralwidget)
        self.down_show_frame.setObjectName(u"down_show_frame")
        self.down_show_frame.setMinimumSize(QSize(300, 100))
        self.down_show_frame.setFont(font1)
        self.down_show_frame.setFrameShape(QFrame.StyledPanel)
        self.down_show_frame.setFrameShadow(QFrame.Sunken)
        self.down_show_layout = QHBoxLayout(self.down_show_frame)
        self.down_show_layout.setObjectName(u"down_show_layout")

        self.gridLayout.addWidget(self.down_show_frame, 1, 1, 1, 1)

        self.three_frame = QFrame(self.centralwidget)
        self.three_frame.setObjectName(u"three_frame")
        self.three_frame.setMinimumSize(QSize(300, 100))
        self.three_frame.setFont(font1)
        self.three_frame.setFrameShape(QFrame.StyledPanel)
        self.three_frame.setFrameShadow(QFrame.Sunken)
        self.three_layout = QHBoxLayout(self.three_frame)
        self.three_layout.setObjectName(u"three_layout")

        self.gridLayout.addWidget(self.three_frame, 1, 2, 1, 1)

        self.up_mark_frame = QFrame(self.centralwidget)
        self.up_mark_frame.setObjectName(u"up_mark_frame")
        self.up_mark_frame.setMinimumSize(QSize(300, 0))
        self.up_mark_frame.setMaximumSize(QSize(800, 60))
        self.up_mark_frame.setFont(font1)
        self.up_mark_frame.setFrameShape(QFrame.NoFrame)
        self.up_mark_frame.setFrameShadow(QFrame.Plain)
        self.up_mark_layout = QHBoxLayout(self.up_mark_frame)
        self.up_mark_layout.setSpacing(0)
        self.up_mark_layout.setObjectName(u"up_mark_layout")
        self.up_mark_layout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.up_mark_frame, 2, 0, 1, 1)

        self.up_show_frame = QFrame(self.centralwidget)
        self.up_show_frame.setObjectName(u"up_show_frame")
        self.up_show_frame.setMinimumSize(QSize(300, 100))
        self.up_show_frame.setFont(font1)
        self.up_show_frame.setFrameShape(QFrame.StyledPanel)
        self.up_show_frame.setFrameShadow(QFrame.Sunken)
        self.up_show_layout = QHBoxLayout(self.up_show_frame)
        self.up_show_layout.setObjectName(u"up_show_layout")

        self.gridLayout.addWidget(self.up_show_frame, 2, 1, 2, 1)

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


        self.gridLayout.addWidget(self.frame_2, 2, 2, 2, 1)

        self.up_frame = QFrame(self.centralwidget)
        self.up_frame.setObjectName(u"up_frame")
        self.up_frame.setMinimumSize(QSize(300, 100))
        self.up_frame.setFont(font1)
        self.up_frame.setFrameShape(QFrame.StyledPanel)
        self.up_frame.setFrameShadow(QFrame.Sunken)
        self.up_layout = QHBoxLayout(self.up_frame)
        self.up_layout.setSpacing(0)
        self.up_layout.setObjectName(u"up_layout")
        self.up_layout.setContentsMargins(9, 9, 9, 9)

        self.gridLayout.addWidget(self.up_frame, 3, 0, 1, 1)

        self.own_mark_frame = QFrame(self.centralwidget)
        self.own_mark_frame.setObjectName(u"own_mark_frame")
        self.own_mark_frame.setMinimumSize(QSize(300, 0))
        self.own_mark_frame.setMaximumSize(QSize(800, 60))
        self.own_mark_frame.setFont(font1)
        self.own_mark_frame.setFrameShape(QFrame.NoFrame)
        self.own_mark_frame.setFrameShadow(QFrame.Plain)
        self.own_mark_layout = QHBoxLayout(self.own_mark_frame)
        self.own_mark_layout.setSpacing(0)
        self.own_mark_layout.setObjectName(u"own_mark_layout")
        self.own_mark_layout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.own_mark_frame, 4, 0, 1, 1)

        self.own_show_frame = QFrame(self.centralwidget)
        self.own_show_frame.setObjectName(u"own_show_frame")
        self.own_show_frame.setMinimumSize(QSize(300, 100))
        self.own_show_frame.setFont(font1)
        self.own_show_frame.setFrameShape(QFrame.StyledPanel)
        self.own_show_frame.setFrameShadow(QFrame.Sunken)
        self.own_show_layout = QHBoxLayout(self.own_show_frame)
        self.own_show_layout.setObjectName(u"own_show_layout")

        self.gridLayout.addWidget(self.own_show_frame, 4, 1, 2, 1)

        self.own_frame = QFrame(self.centralwidget)
        self.own_frame.setObjectName(u"own_frame")
        self.own_frame.setMinimumSize(QSize(300, 100))
        self.own_frame.setFont(font1)
        self.own_frame.setFrameShape(QFrame.StyledPanel)
        self.own_frame.setFrameShadow(QFrame.Sunken)
        self.own_layout = QHBoxLayout(self.own_frame)
        self.own_layout.setSpacing(0)
        self.own_layout.setObjectName(u"own_layout")
        self.own_layout.setContentsMargins(9, 9, 9, 9)

        self.gridLayout.addWidget(self.own_frame, 5, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 930, 22))
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

