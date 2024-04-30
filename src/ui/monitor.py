# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'monitor.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_Monitor(object):
    def setupUi(self, Monitor):
        if not Monitor.objectName():
            Monitor.setObjectName(u"Monitor")
        Monitor.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(Monitor)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.image = QLabel(Monitor)
        self.image.setObjectName(u"image")
        font = QFont()
        font.setFamilies([u"DengXian"])
        font.setPointSize(14)
        self.image.setFont(font)
        self.image.setScaledContents(True)
        self.image.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.image)


        self.retranslateUi(Monitor)

        QMetaObject.connectSlotsByName(Monitor)
    # setupUi

    def retranslateUi(self, Monitor):
        Monitor.setWindowTitle(QCoreApplication.translate("Monitor", u"Form", None))
        self.image.setText(QCoreApplication.translate("Monitor", u"Capture Image", None))
    # retranslateUi

