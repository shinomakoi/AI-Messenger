# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'character_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_CharacterForm(object):
    def setupUi(self, CharacterForm):
        if not CharacterForm.objectName():
            CharacterForm.setObjectName(u"CharacterForm")
        CharacterForm.resize(674, 856)
        self.gridLayout = QGridLayout(CharacterForm)
        self.gridLayout.setObjectName(u"gridLayout")
        self.saveButton = QPushButton(CharacterForm)
        self.saveButton.setObjectName(u"saveButton")

        self.gridLayout.addWidget(self.saveButton, 7, 0, 1, 1)

        self.charExampleDialog = QPlainTextEdit(CharacterForm)
        self.charExampleDialog.setObjectName(u"charExampleDialog")

        self.gridLayout.addWidget(self.charExampleDialog, 3, 0, 1, 1)

        self.charScenario = QPlainTextEdit(CharacterForm)
        self.charScenario.setObjectName(u"charScenario")

        self.gridLayout.addWidget(self.charScenario, 2, 0, 1, 1)

        self.charName = QLineEdit(CharacterForm)
        self.charName.setObjectName(u"charName")

        self.gridLayout.addWidget(self.charName, 0, 0, 1, 1)

        self.charTags = QLineEdit(CharacterForm)
        self.charTags.setObjectName(u"charTags")

        self.gridLayout.addWidget(self.charTags, 5, 0, 1, 1)

        self.charPersona = QPlainTextEdit(CharacterForm)
        self.charPersona.setObjectName(u"charPersona")

        self.gridLayout.addWidget(self.charPersona, 1, 0, 1, 1)

        self.charTemplate = QLineEdit(CharacterForm)
        self.charTemplate.setObjectName(u"charTemplate")

        self.gridLayout.addWidget(self.charTemplate, 6, 0, 1, 1)


        self.retranslateUi(CharacterForm)

        QMetaObject.connectSlotsByName(CharacterForm)
    # setupUi

    def retranslateUi(self, CharacterForm):
        CharacterForm.setWindowTitle(QCoreApplication.translate("CharacterForm", u"Character create", None))
        self.saveButton.setText(QCoreApplication.translate("CharacterForm", u"Save", None))
        self.charExampleDialog.setPlaceholderText(QCoreApplication.translate("CharacterForm", u"Example dialog", None))
#if QT_CONFIG(tooltip)
        self.charScenario.setToolTip(QCoreApplication.translate("CharacterForm", u"Use {{char}} as user name placeholder", None))
#endif // QT_CONFIG(tooltip)
        self.charScenario.setPlaceholderText(QCoreApplication.translate("CharacterForm", u"Scenario", None))
#if QT_CONFIG(tooltip)
        self.charName.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.charName.setPlaceholderText(QCoreApplication.translate("CharacterForm", u"Character's name", None))
        self.charTags.setPlaceholderText(QCoreApplication.translate("CharacterForm", u"Tags", None))
        self.charPersona.setPlaceholderText(QCoreApplication.translate("CharacterForm", u"Character's personality", None))
        self.charTemplate.setText("")
        self.charTemplate.setPlaceholderText(QCoreApplication.translate("CharacterForm", u"Turn template (leave empty for default)", None))
    # retranslateUi

