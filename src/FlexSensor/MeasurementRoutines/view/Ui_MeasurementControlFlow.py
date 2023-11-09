# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MeasurementControlFlow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QListView, QSizePolicy,
    QWidget)

class Ui_MeasurementControlFlow(object):
    def setupUi(self, MeasurementControlFlow):
        if not MeasurementControlFlow.objectName():
            MeasurementControlFlow.setObjectName(u"MeasurementControlFlow")
        MeasurementControlFlow.resize(400, 300)
        self.gridLayout_2 = QGridLayout(MeasurementControlFlow)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.listView_control_flow = QListView(MeasurementControlFlow)
        self.listView_control_flow.setObjectName(u"listView_control_flow")

        self.gridLayout.addWidget(self.listView_control_flow, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(MeasurementControlFlow)

        QMetaObject.connectSlotsByName(MeasurementControlFlow)
    # setupUi

    def retranslateUi(self, MeasurementControlFlow):
        MeasurementControlFlow.setWindowTitle(QCoreApplication.translate("MeasurementControlFlow", u"Form", None))
    # retranslateUi

