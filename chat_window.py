# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chat_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QSplitter, QStatusBar, QTabWidget,
    QTextEdit, QToolBox, QToolButton, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_ChatWindow(object):
    def setupUi(self, ChatWindow):
        if not ChatWindow.objectName():
            ChatWindow.setObjectName(u"ChatWindow")
        ChatWindow.resize(1582, 1117)
        self.actionSettings = QAction(ChatWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionExit = QAction(ChatWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAbout = QAction(ChatWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionSave_settings = QAction(ChatWindow)
        self.actionSave_settings.setObjectName(u"actionSave_settings")
        self.actionSave_session = QAction(ChatWindow)
        self.actionSave_session.setObjectName(u"actionSave_session")
        self.actionReload_contacts = QAction(ChatWindow)
        self.actionReload_contacts.setObjectName(u"actionReload_contacts")
        self.actionCharacter = QAction(ChatWindow)
        self.actionCharacter.setObjectName(u"actionCharacter")
        self.actionLoad_session = QAction(ChatWindow)
        self.actionLoad_session.setObjectName(u"actionLoad_session")
        self.centralwidget = QWidget(ChatWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.retryButton = QPushButton(self.centralwidget)
        self.retryButton.setObjectName(u"retryButton")
        self.retryButton.setEnabled(False)
        self.retryButton.setMinimumSize(QSize(64, 64))
        self.retryButton.setMaximumSize(QSize(64, 64))

        self.gridLayout_5.addWidget(self.retryButton, 2, 2, 1, 1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.textTabWidget = QTabWidget(self.splitter)
        self.textTabWidget.setObjectName(u"textTabWidget")
        self.chatTab = QWidget()
        self.chatTab.setObjectName(u"chatTab")
        self.gridLayout = QGridLayout(self.chatTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter_2 = QSplitter(self.chatTab)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.contactsTree = QTreeWidget(self.splitter_2)
        self.contactsTree.setObjectName(u"contactsTree")
        self.contactsTree.setMaximumSize(QSize(256, 16777215))
        self.contactsTree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.splitter_2.addWidget(self.contactsTree)
        self.chatTextEdit = QTextEdit(self.splitter_2)
        self.chatTextEdit.setObjectName(u"chatTextEdit")
        self.chatTextEdit.setReadOnly(True)
        self.chatTextEdit.setAcceptRichText(False)
        self.splitter_2.addWidget(self.chatTextEdit)

        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.textTabWidget.addTab(self.chatTab, "")
        self.notebookTab = QWidget()
        self.notebookTab.setObjectName(u"notebookTab")
        self.gridLayout_6 = QGridLayout(self.notebookTab)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.notebookTextEdit = QTextEdit(self.notebookTab)
        self.notebookTextEdit.setObjectName(u"notebookTextEdit")
        self.notebookTextEdit.setAcceptRichText(False)

        self.gridLayout_6.addWidget(self.notebookTextEdit, 0, 0, 1, 1)

        self.textTabWidget.addTab(self.notebookTab, "")
        self.splitter.addWidget(self.textTabWidget)
        self.rightToolbox = QToolBox(self.splitter)
        self.rightToolbox.setObjectName(u"rightToolbox")
        self.rightToolbox.setMaximumSize(QSize(256, 16777215))
        self.paramsBasicPage = QWidget()
        self.paramsBasicPage.setObjectName(u"paramsBasicPage")
        self.paramsBasicPage.setGeometry(QRect(0, 0, 256, 831))
        self.gridLayout_2 = QGridLayout(self.paramsBasicPage)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_5 = QLabel(self.paramsBasicPage)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_8 = QLabel(self.paramsBasicPage)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 12, 0, 1, 2)

        self.label_11 = QLabel(self.paramsBasicPage)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 8, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 14, 0, 1, 3)

        self.top_pSpin = QDoubleSpinBox(self.paramsBasicPage)
        self.top_pSpin.setObjectName(u"top_pSpin")
        self.top_pSpin.setMaximum(1.000000000000000)
        self.top_pSpin.setSingleStep(0.010000000000000)
        self.top_pSpin.setValue(0.900000000000000)

        self.gridLayout_2.addWidget(self.top_pSpin, 7, 2, 1, 1)

        self.label_15 = QLabel(self.paramsBasicPage)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 2, 0, 1, 1)

        self.top_pSlider = QSlider(self.paramsBasicPage)
        self.top_pSlider.setObjectName(u"top_pSlider")
        self.top_pSlider.setMaximum(100)
        self.top_pSlider.setValue(90)
        self.top_pSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.top_pSlider, 7, 0, 1, 2)

        self.max_new_tokensSpin = QSpinBox(self.paramsBasicPage)
        self.max_new_tokensSpin.setObjectName(u"max_new_tokensSpin")
        self.max_new_tokensSpin.setMinimum(-2)
        self.max_new_tokensSpin.setMaximum(4096)
        self.max_new_tokensSpin.setSingleStep(64)
        self.max_new_tokensSpin.setValue(512)

        self.gridLayout_2.addWidget(self.max_new_tokensSpin, 9, 2, 1, 1)

        self.label_17 = QLabel(self.paramsBasicPage)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_2.addWidget(self.label_17, 6, 0, 1, 1)

        self.temperatureSlider = QSlider(self.paramsBasicPage)
        self.temperatureSlider.setObjectName(u"temperatureSlider")
        self.temperatureSlider.setMaximum(400)
        self.temperatureSlider.setValue(70)
        self.temperatureSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.temperatureSlider, 3, 0, 1, 2)

        self.max_new_tokensSlider = QSlider(self.paramsBasicPage)
        self.max_new_tokensSlider.setObjectName(u"max_new_tokensSlider")
        self.max_new_tokensSlider.setMinimum(-2)
        self.max_new_tokensSlider.setMaximum(4096)
        self.max_new_tokensSlider.setPageStep(32)
        self.max_new_tokensSlider.setValue(512)
        self.max_new_tokensSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.max_new_tokensSlider, 9, 0, 1, 2)

        self.typical_pSlider = QSlider(self.paramsBasicPage)
        self.typical_pSlider.setObjectName(u"typical_pSlider")
        self.typical_pSlider.setMinimum(1)
        self.typical_pSlider.setMaximum(100)
        self.typical_pSlider.setValue(100)
        self.typical_pSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.typical_pSlider, 13, 0, 1, 1)

        self.repetition_penaltySpin = QDoubleSpinBox(self.paramsBasicPage)
        self.repetition_penaltySpin.setObjectName(u"repetition_penaltySpin")
        self.repetition_penaltySpin.setMinimum(1.000000000000000)
        self.repetition_penaltySpin.setMaximum(1.800000000000000)
        self.repetition_penaltySpin.setSingleStep(0.010000000000000)
        self.repetition_penaltySpin.setValue(1.120000000000000)

        self.gridLayout_2.addWidget(self.repetition_penaltySpin, 11, 2, 1, 1)

        self.temperatureSpin = QDoubleSpinBox(self.paramsBasicPage)
        self.temperatureSpin.setObjectName(u"temperatureSpin")
        self.temperatureSpin.setMaximum(4.000000000000000)
        self.temperatureSpin.setSingleStep(0.010000000000000)
        self.temperatureSpin.setValue(0.700000000000000)

        self.gridLayout_2.addWidget(self.temperatureSpin, 3, 2, 1, 1)

        self.paramPresets_comboBox = QComboBox(self.paramsBasicPage)
        self.paramPresets_comboBox.setObjectName(u"paramPresets_comboBox")
        self.paramPresets_comboBox.setInsertPolicy(QComboBox.InsertAlphabetically)

        self.gridLayout_2.addWidget(self.paramPresets_comboBox, 1, 0, 1, 3)

        self.repetition_penaltySlider = QSlider(self.paramsBasicPage)
        self.repetition_penaltySlider.setObjectName(u"repetition_penaltySlider")
        self.repetition_penaltySlider.setMinimum(100)
        self.repetition_penaltySlider.setMaximum(180)
        self.repetition_penaltySlider.setValue(120)
        self.repetition_penaltySlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.repetition_penaltySlider, 11, 0, 1, 2)

        self.label_2 = QLabel(self.paramsBasicPage)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.typical_pSpin = QDoubleSpinBox(self.paramsBasicPage)
        self.typical_pSpin.setObjectName(u"typical_pSpin")
        self.typical_pSpin.setMinimum(0.010000000000000)
        self.typical_pSpin.setMaximum(1.000000000000000)
        self.typical_pSpin.setSingleStep(0.010000000000000)
        self.typical_pSpin.setValue(1.000000000000000)

        self.gridLayout_2.addWidget(self.typical_pSpin, 13, 2, 1, 1)

        self.top_kSlider = QSlider(self.paramsBasicPage)
        self.top_kSlider.setObjectName(u"top_kSlider")
        self.top_kSlider.setMaximum(200)
        self.top_kSlider.setValue(20)
        self.top_kSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.top_kSlider, 5, 0, 1, 2)

        self.top_kSpin = QSpinBox(self.paramsBasicPage)
        self.top_kSpin.setObjectName(u"top_kSpin")
        self.top_kSpin.setMaximum(200)
        self.top_kSpin.setValue(20)

        self.gridLayout_2.addWidget(self.top_kSpin, 5, 2, 1, 1)

        self.label = QLabel(self.paramsBasicPage)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 10, 0, 1, 2)

        self.rightToolbox.addItem(self.paramsBasicPage, u"Params - Shared")
        self.paramAdvPage = QWidget()
        self.paramAdvPage.setObjectName(u"paramAdvPage")
        self.paramAdvPage.setGeometry(QRect(0, 0, 256, 831))
        self.gridLayout_4 = QGridLayout(self.paramAdvPage)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.tfszSlider = QSlider(self.paramAdvPage)
        self.tfszSlider.setObjectName(u"tfszSlider")
        self.tfszSlider.setMinimum(1)
        self.tfszSlider.setMaximum(100)
        self.tfszSlider.setValue(100)
        self.tfszSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.tfszSlider, 10, 0, 1, 1)

        self.label_9 = QLabel(self.paramAdvPage)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 16, 0, 1, 1)

        self.label_4 = QLabel(self.paramAdvPage)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 5, 0, 1, 1)

        self.tfszSpin = QDoubleSpinBox(self.paramAdvPage)
        self.tfszSpin.setObjectName(u"tfszSpin")
        self.tfszSpin.setMinimum(0.010000000000000)
        self.tfszSpin.setMaximum(1.000000000000000)
        self.tfszSpin.setSingleStep(0.010000000000000)
        self.tfszSpin.setValue(1.000000000000000)

        self.gridLayout_4.addWidget(self.tfszSpin, 10, 1, 1, 1)

        self.keepLastNSlider = QSlider(self.paramAdvPage)
        self.keepLastNSlider.setObjectName(u"keepLastNSlider")
        self.keepLastNSlider.setMinimum(-1)
        self.keepLastNSlider.setMaximum(8192)
        self.keepLastNSlider.setValue(2048)
        self.keepLastNSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.keepLastNSlider, 3, 0, 1, 1)

        self.label_20 = QLabel(self.paramAdvPage)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_4.addWidget(self.label_20, 2, 0, 1, 1)

        self.presencePenaltySpin = QDoubleSpinBox(self.paramAdvPage)
        self.presencePenaltySpin.setObjectName(u"presencePenaltySpin")
        self.presencePenaltySpin.setMaximum(3.000000000000000)
        self.presencePenaltySpin.setSingleStep(0.010000000000000)

        self.gridLayout_4.addWidget(self.presencePenaltySpin, 8, 1, 1, 1)

        self.label_3 = QLabel(self.paramAdvPage)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 15, 0, 1, 1)

        self.keepLastNSpin = QSpinBox(self.paramAdvPage)
        self.keepLastNSpin.setObjectName(u"keepLastNSpin")
        self.keepLastNSpin.setMinimum(-1)
        self.keepLastNSpin.setMaximum(8192)
        self.keepLastNSpin.setValue(2048)

        self.gridLayout_4.addWidget(self.keepLastNSpin, 3, 1, 1, 1)

        self.mirostatEta = QSpinBox(self.paramAdvPage)
        self.mirostatEta.setObjectName(u"mirostatEta")
        self.mirostatEta.setMaximum(2)

        self.gridLayout_4.addWidget(self.mirostatEta, 14, 1, 1, 1)

        self.label_31 = QLabel(self.paramAdvPage)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_4.addWidget(self.label_31, 9, 0, 1, 1)

        self.line_2 = QFrame(self.paramAdvPage)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.line_2, 13, 0, 1, 1)

        self.label_14 = QLabel(self.paramAdvPage)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_4.addWidget(self.label_14, 14, 0, 1, 1)

        self.label_7 = QLabel(self.paramAdvPage)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 7, 0, 1, 1)

        self.repeatLastSlider = QSlider(self.paramAdvPage)
        self.repeatLastSlider.setObjectName(u"repeatLastSlider")
        self.repeatLastSlider.setMinimum(-1)
        self.repeatLastSlider.setMaximum(2048)
        self.repeatLastSlider.setValue(256)
        self.repeatLastSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.repeatLastSlider, 1, 0, 1, 1)

        self.minPSlider = QSlider(self.paramAdvPage)
        self.minPSlider.setObjectName(u"minPSlider")
        self.minPSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.minPSlider, 12, 0, 1, 1)

        self.seedSpin = QSpinBox(self.paramAdvPage)
        self.seedSpin.setObjectName(u"seedSpin")
        self.seedSpin.setMinimum(-1)
        self.seedSpin.setMaximum(999999999)
        self.seedSpin.setValue(-1)

        self.gridLayout_4.addWidget(self.seedSpin, 19, 0, 1, 1)

        self.line = QFrame(self.paramAdvPage)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.line, 4, 0, 1, 1)

        self.freqPenaltySpin = QDoubleSpinBox(self.paramAdvPage)
        self.freqPenaltySpin.setObjectName(u"freqPenaltySpin")
        self.freqPenaltySpin.setMaximum(3.000000000000000)
        self.freqPenaltySpin.setSingleStep(0.010000000000000)

        self.gridLayout_4.addWidget(self.freqPenaltySpin, 6, 1, 1, 1)

        self.presencePenaltySlider = QSlider(self.paramAdvPage)
        self.presencePenaltySlider.setObjectName(u"presencePenaltySlider")
        self.presencePenaltySlider.setMaximum(300)
        self.presencePenaltySlider.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.presencePenaltySlider, 8, 0, 1, 1)

        self.label_6 = QLabel(self.paramAdvPage)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 11, 0, 1, 1)

        self.label_19 = QLabel(self.paramAdvPage)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_4.addWidget(self.label_19, 0, 0, 1, 1)

        self.mirostatTau = QSpinBox(self.paramAdvPage)
        self.mirostatTau.setObjectName(u"mirostatTau")
        self.mirostatTau.setMinimum(2)
        self.mirostatTau.setMaximum(12)
        self.mirostatTau.setValue(5)

        self.gridLayout_4.addWidget(self.mirostatTau, 15, 1, 1, 1)

        self.mirostatMode = QDoubleSpinBox(self.paramAdvPage)
        self.mirostatMode.setObjectName(u"mirostatMode")
        self.mirostatMode.setMaximum(2.000000000000000)
        self.mirostatMode.setSingleStep(0.010000000000000)
        self.mirostatMode.setValue(0.100000000000000)

        self.gridLayout_4.addWidget(self.mirostatMode, 16, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 718, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 20, 0, 1, 2)

        self.repeatLastSpin = QSpinBox(self.paramAdvPage)
        self.repeatLastSpin.setObjectName(u"repeatLastSpin")
        self.repeatLastSpin.setMinimum(-1)
        self.repeatLastSpin.setMaximum(2048)
        self.repeatLastSpin.setValue(256)

        self.gridLayout_4.addWidget(self.repeatLastSpin, 1, 1, 1, 1)

        self.minpSpin = QDoubleSpinBox(self.paramAdvPage)
        self.minpSpin.setObjectName(u"minpSpin")
        self.minpSpin.setMaximum(1.000000000000000)
        self.minpSpin.setSingleStep(0.010000000000000)
        self.minpSpin.setValue(0.100000000000000)

        self.gridLayout_4.addWidget(self.minpSpin, 12, 1, 1, 1)

        self.label_21 = QLabel(self.paramAdvPage)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_4.addWidget(self.label_21, 18, 0, 1, 1)

        self.freqPenaltySlider = QSlider(self.paramAdvPage)
        self.freqPenaltySlider.setObjectName(u"freqPenaltySlider")
        self.freqPenaltySlider.setMaximum(300)
        self.freqPenaltySlider.setValue(0)
        self.freqPenaltySlider.setOrientation(Qt.Horizontal)

        self.gridLayout_4.addWidget(self.freqPenaltySlider, 6, 0, 1, 1)

        self.line_3 = QFrame(self.paramAdvPage)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.line_3, 17, 0, 1, 1)

        self.rightToolbox.addItem(self.paramAdvPage, u"Params - More")
        self.preferencesPage = QWidget()
        self.preferencesPage.setObjectName(u"preferencesPage")
        self.preferencesPage.setGeometry(QRect(0, 0, 256, 831))
        self.gridLayout_3 = QGridLayout(self.preferencesPage)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.customSysPromptCheck = QCheckBox(self.preferencesPage)
        self.customSysPromptCheck.setObjectName(u"customSysPromptCheck")

        self.gridLayout_3.addWidget(self.customSysPromptCheck, 9, 0, 1, 1)

        self.botnameLine = QLineEdit(self.preferencesPage)
        self.botnameLine.setObjectName(u"botnameLine")

        self.gridLayout_3.addWidget(self.botnameLine, 6, 0, 1, 1)

        self.usernameLine = QLineEdit(self.preferencesPage)
        self.usernameLine.setObjectName(u"usernameLine")
        self.usernameLine.setFrame(True)
        self.usernameLine.setClearButtonEnabled(False)

        self.gridLayout_3.addWidget(self.usernameLine, 4, 0, 1, 1)

        self.customSysPromptText = QPlainTextEdit(self.preferencesPage)
        self.customSysPromptText.setObjectName(u"customSysPromptText")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customSysPromptText.sizePolicy().hasHeightForWidth())
        self.customSysPromptText.setSizePolicy(sizePolicy)
        self.customSysPromptText.setMinimumSize(QSize(0, 168))

        self.gridLayout_3.addWidget(self.customSysPromptText, 10, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 493, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 14, 0, 1, 1)

        self.streamCheck = QCheckBox(self.preferencesPage)
        self.streamCheck.setObjectName(u"streamCheck")
        self.streamCheck.setChecked(True)

        self.gridLayout_3.addWidget(self.streamCheck, 1, 0, 1, 1)

        self.cacheCheck = QCheckBox(self.preferencesPage)
        self.cacheCheck.setObjectName(u"cacheCheck")
        self.cacheCheck.setChecked(True)

        self.gridLayout_3.addWidget(self.cacheCheck, 2, 0, 1, 1)

        self.label_12 = QLabel(self.preferencesPage)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_3.addWidget(self.label_12, 5, 0, 1, 1)

        self.label_10 = QLabel(self.preferencesPage)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 3, 0, 1, 1)

        self.groupBox = QGroupBox(self.preferencesPage)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.backendCppCheck = QRadioButton(self.groupBox)
        self.backendCppCheck.setObjectName(u"backendCppCheck")
        self.backendCppCheck.setChecked(True)

        self.verticalLayout.addWidget(self.backendCppCheck)

        self.backendExllamaCheck = QRadioButton(self.groupBox)
        self.backendExllamaCheck.setObjectName(u"backendExllamaCheck")

        self.verticalLayout.addWidget(self.backendExllamaCheck)


        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.rightToolbox.addItem(self.preferencesPage, u"Preferences")
        self.themesPage = QWidget()
        self.themesPage.setObjectName(u"themesPage")
        self.themesPage.setGeometry(QRect(0, 0, 256, 831))
        self.gridLayout_7 = QGridLayout(self.themesPage)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.custStopStringLine = QLineEdit(self.themesPage)
        self.custStopStringLine.setObjectName(u"custStopStringLine")

        self.gridLayout_7.addWidget(self.custStopStringLine, 5, 0, 1, 1)

        self.stopStringAutoCheck = QCheckBox(self.themesPage)
        self.stopStringAutoCheck.setObjectName(u"stopStringAutoCheck")
        self.stopStringAutoCheck.setChecked(True)

        self.gridLayout_7.addWidget(self.stopStringAutoCheck, 1, 0, 1, 1)

        self.label_13 = QLabel(self.themesPage)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_7.addWidget(self.label_13, 6, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_5, 11, 0, 1, 1)

        self.penaliseNlCheck = QCheckBox(self.themesPage)
        self.penaliseNlCheck.setObjectName(u"penaliseNlCheck")

        self.gridLayout_7.addWidget(self.penaliseNlCheck, 8, 0, 1, 1)

        self.label_16 = QLabel(self.themesPage)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_7.addWidget(self.label_16, 4, 0, 1, 1)

        self.autoSaveSessionCheck = QCheckBox(self.themesPage)
        self.autoSaveSessionCheck.setObjectName(u"autoSaveSessionCheck")
        self.autoSaveSessionCheck.setChecked(True)

        self.gridLayout_7.addWidget(self.autoSaveSessionCheck, 2, 0, 1, 1)

        self.imgFileLine = QLineEdit(self.themesPage)
        self.imgFileLine.setObjectName(u"imgFileLine")

        self.gridLayout_7.addWidget(self.imgFileLine, 7, 0, 1, 1)

        self.autoscrollCheck = QCheckBox(self.themesPage)
        self.autoscrollCheck.setObjectName(u"autoscrollCheck")
        self.autoscrollCheck.setChecked(True)

        self.gridLayout_7.addWidget(self.autoscrollCheck, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.themesPage)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_8 = QGridLayout(self.groupBox_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.themeNativeRadio = QRadioButton(self.groupBox_2)
        self.themeNativeRadio.setObjectName(u"themeNativeRadio")

        self.gridLayout_8.addWidget(self.themeNativeRadio, 4, 0, 1, 1)

        self.themeDarkRadio = QRadioButton(self.groupBox_2)
        self.themeDarkRadio.setObjectName(u"themeDarkRadio")
        self.themeDarkRadio.setChecked(True)

        self.gridLayout_8.addWidget(self.themeDarkRadio, 2, 0, 1, 1)

        self.themeLightRadio = QRadioButton(self.groupBox_2)
        self.themeLightRadio.setObjectName(u"themeLightRadio")

        self.gridLayout_8.addWidget(self.themeLightRadio, 3, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupBox_2, 9, 0, 1, 1)

        self.imgFileButton = QToolButton(self.themesPage)
        self.imgFileButton.setObjectName(u"imgFileButton")

        self.gridLayout_7.addWidget(self.imgFileButton, 7, 1, 1, 1)

        self.rightToolbox.addItem(self.themesPage, u"Preferences - More")
        self.splitter.addWidget(self.rightToolbox)

        self.gridLayout_5.addWidget(self.splitter, 0, 0, 1, 7)

        self.inputHistoryCombo = QComboBox(self.centralwidget)
        self.inputHistoryCombo.setObjectName(u"inputHistoryCombo")

        self.gridLayout_5.addWidget(self.inputHistoryCombo, 1, 0, 1, 1)

        self.clearButton = QPushButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setEnabled(False)
        self.clearButton.setMinimumSize(QSize(64, 64))
        self.clearButton.setMaximumSize(QSize(64, 64))

        self.gridLayout_5.addWidget(self.clearButton, 2, 5, 1, 1)

        self.generateButton = QPushButton(self.centralwidget)
        self.generateButton.setObjectName(u"generateButton")
        self.generateButton.setEnabled(True)
        self.generateButton.setMinimumSize(QSize(64, 64))
        self.generateButton.setMaximumSize(QSize(64, 64))

        self.gridLayout_5.addWidget(self.generateButton, 2, 1, 1, 1)

        self.continueButton = QPushButton(self.centralwidget)
        self.continueButton.setObjectName(u"continueButton")
        self.continueButton.setEnabled(False)
        self.continueButton.setMinimumSize(QSize(64, 64))
        self.continueButton.setMaximumSize(QSize(64, 64))

        self.gridLayout_5.addWidget(self.continueButton, 2, 4, 1, 1)

        self.rewindButton = QPushButton(self.centralwidget)
        self.rewindButton.setObjectName(u"rewindButton")
        self.rewindButton.setEnabled(False)
        self.rewindButton.setMinimumSize(QSize(64, 64))
        self.rewindButton.setMaximumSize(QSize(64, 64))

        self.gridLayout_5.addWidget(self.rewindButton, 2, 3, 1, 1)

        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setEnabled(False)
        self.stopButton.setMinimumSize(QSize(64, 64))
        self.stopButton.setMaximumSize(QSize(64, 64))

        self.gridLayout_5.addWidget(self.stopButton, 2, 6, 1, 1)

        ChatWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ChatWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1582, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuEditors = QMenu(self.menubar)
        self.menuEditors.setObjectName(u"menuEditors")
        ChatWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ChatWindow)
        self.statusbar.setObjectName(u"statusbar")
        ChatWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEditors.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionReload_contacts)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_session)
        self.menuFile.addAction(self.actionLoad_session)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_settings)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuEditors.addAction(self.actionCharacter)

        self.retranslateUi(ChatWindow)
        self.top_kSlider.valueChanged.connect(self.top_kSpin.setValue)
        self.max_new_tokensSpin.valueChanged.connect(self.max_new_tokensSlider.setValue)
        self.max_new_tokensSlider.valueChanged.connect(self.max_new_tokensSpin.setValue)
        self.top_kSpin.valueChanged.connect(self.top_kSlider.setValue)
        self.repeatLastSlider.valueChanged.connect(self.repeatLastSpin.setValue)
        self.repeatLastSpin.valueChanged.connect(self.repeatLastSlider.setValue)
        self.keepLastNSlider.valueChanged.connect(self.keepLastNSpin.setValue)
        self.keepLastNSpin.valueChanged.connect(self.keepLastNSlider.setValue)

        self.textTabWidget.setCurrentIndex(0)
        self.rightToolbox.setCurrentIndex(0)
        self.generateButton.setDefault(True)


        QMetaObject.connectSlotsByName(ChatWindow)
    # setupUi

    def retranslateUi(self, ChatWindow):
        ChatWindow.setWindowTitle(QCoreApplication.translate("ChatWindow", u"AI Messenger", None))
        self.actionSettings.setText(QCoreApplication.translate("ChatWindow", u"Settings", None))
        self.actionExit.setText(QCoreApplication.translate("ChatWindow", u"Exit", None))
        self.actionAbout.setText(QCoreApplication.translate("ChatWindow", u"About", None))
        self.actionSave_settings.setText(QCoreApplication.translate("ChatWindow", u"Save settings", None))
        self.actionSave_session.setText(QCoreApplication.translate("ChatWindow", u"Save session", None))
        self.actionReload_contacts.setText(QCoreApplication.translate("ChatWindow", u"Reload contacts", None))
        self.actionCharacter.setText(QCoreApplication.translate("ChatWindow", u"Character", None))
        self.actionLoad_session.setText(QCoreApplication.translate("ChatWindow", u"Load session", None))
#if QT_CONFIG(tooltip)
        self.retryButton.setToolTip(QCoreApplication.translate("ChatWindow", u"Retry", None))
#endif // QT_CONFIG(tooltip)
        self.retryButton.setText(QCoreApplication.translate("ChatWindow", u"Ret", None))
        ___qtreewidgetitem = self.contactsTree.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("ChatWindow", u"Contacts", None));
        self.chatTextEdit.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"Output text", None))
        self.textTabWidget.setTabText(self.textTabWidget.indexOf(self.chatTab), QCoreApplication.translate("ChatWindow", u"Chat", None))
        self.notebookTextEdit.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"Output text", None))
        self.textTabWidget.setTabText(self.textTabWidget.indexOf(self.notebookTab), QCoreApplication.translate("ChatWindow", u"Notebook", None))
        self.label_5.setText(QCoreApplication.translate("ChatWindow", u"Top K:", None))
        self.label_8.setText(QCoreApplication.translate("ChatWindow", u"Typical P:", None))
        self.label_11.setText(QCoreApplication.translate("ChatWindow", u"Max new tokens:", None))
#if QT_CONFIG(tooltip)
        self.top_pSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Limit the next token selection to a subset of tokens with a cumulative probability above a threshold P", None))
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("ChatWindow", u"Temperature:", None))
#if QT_CONFIG(tooltip)
        self.top_pSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Limit the next token selection to a subset of tokens with a cumulative probability above a threshold P", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.max_new_tokensSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Set the number of tokens to predict when generating text (-1 = infinity, -2 = until context filled)", None))
#endif // QT_CONFIG(tooltip)
        self.label_17.setText(QCoreApplication.translate("ChatWindow", u"Top P:", None))
#if QT_CONFIG(tooltip)
        self.temperatureSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Adjust the randomness of the generated text", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.max_new_tokensSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Set the number of tokens to predict when generating text (-1 = infinity, -2 = until context filled)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.typical_pSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Locally typical sampling, parameter p (1.0 = disabled)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.repetition_penaltySpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Repetition penality value", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.temperatureSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Adjust the randomness of the generated text", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.paramPresets_comboBox.setToolTip(QCoreApplication.translate("ChatWindow", u"Parameter preset", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.repetition_penaltySlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Repetition penality value", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("ChatWindow", u"Preset:", None))
#if QT_CONFIG(tooltip)
        self.typical_pSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Locally typical sampling, parameter p (1.0 = disabled)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.top_kSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Limit the next token selection to the K most probable tokens", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.top_kSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Limit the next token selection to the K most probable tokens", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("ChatWindow", u"Repetition penalty:", None))
        self.rightToolbox.setItemText(self.rightToolbox.indexOf(self.paramsBasicPage), QCoreApplication.translate("ChatWindow", u"Params - Shared", None))
#if QT_CONFIG(tooltip)
        self.tfszSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Tail free sampling, parameter z (1.0 = disabled)", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("ChatWindow", u"Mirostat LR:", None))
        self.label_4.setText(QCoreApplication.translate("ChatWindow", u"Frequency penalty:", None))
#if QT_CONFIG(tooltip)
        self.tfszSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Tail free sampling, parameter z (1.0 = disabled)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.keepLastNSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Keep this many tokens when context exceeded (-1 = all)", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("ChatWindow", u"Keep prompt n:", None))
#if QT_CONFIG(tooltip)
        self.presencePenaltySpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Repeat alpha presence penalty (0.0 = disabled)", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("ChatWindow", u"Mirostat Ent:", None))
#if QT_CONFIG(tooltip)
        self.keepLastNSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Keep this many tokens when context exceeded (-1 = all)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mirostatEta.setToolTip(QCoreApplication.translate("ChatWindow", u"Use Mirostat sampling. Top K, Nucleus, Tail Free and Locally Typical samplers are ignored if used. (0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)", None))
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(QCoreApplication.translate("ChatWindow", u"Tail Free Sampling:", None))
        self.label_14.setText(QCoreApplication.translate("ChatWindow", u"Mirostat mode:", None))
        self.label_7.setText(QCoreApplication.translate("ChatWindow", u"Presence penalty:", None))
#if QT_CONFIG(tooltip)
        self.repeatLastSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Range to sample for repeat penalty (-1 = all)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.minPSlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Sets a minimum base probability threshold for token selection", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.seedSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Seed value (-1 for random)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.freqPenaltySpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Repeat alpha frequency penalty (0.0 = disabled)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.presencePenaltySlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Repeat alpha presence penalty (0.0 = disabled)", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("ChatWindow", u"Min P:", None))
        self.label_19.setText(QCoreApplication.translate("ChatWindow", u"Repeat last n:", None))
#if QT_CONFIG(tooltip)
        self.mirostatTau.setToolTip(QCoreApplication.translate("ChatWindow", u"Set the Mirostat target entropy, parameter tau", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mirostatMode.setToolTip(QCoreApplication.translate("ChatWindow", u"Set the Mirostat learning rate, parameter eta", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.repeatLastSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Range to sample for repeat penalty (-1 = all)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.minpSpin.setToolTip(QCoreApplication.translate("ChatWindow", u"Sets a minimum base probability threshold for token selection", None))
#endif // QT_CONFIG(tooltip)
        self.label_21.setText(QCoreApplication.translate("ChatWindow", u"Seed:", None))
#if QT_CONFIG(tooltip)
        self.freqPenaltySlider.setToolTip(QCoreApplication.translate("ChatWindow", u"Repeat alpha frequency penalty (0.0 = disabled)", None))
#endif // QT_CONFIG(tooltip)
        self.rightToolbox.setItemText(self.rightToolbox.indexOf(self.paramAdvPage), QCoreApplication.translate("ChatWindow", u"Params - More", None))
#if QT_CONFIG(tooltip)
        self.customSysPromptCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Use a custom system prompt", None))
#endif // QT_CONFIG(tooltip)
        self.customSysPromptCheck.setText(QCoreApplication.translate("ChatWindow", u"System prompt:", None))
#if QT_CONFIG(tooltip)
        self.botnameLine.setToolTip(QCoreApplication.translate("ChatWindow", u"Display name of bot", None))
#endif // QT_CONFIG(tooltip)
        self.botnameLine.setText(QCoreApplication.translate("ChatWindow", u"Bot", None))
        self.botnameLine.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"Bot", None))
#if QT_CONFIG(tooltip)
        self.usernameLine.setToolTip(QCoreApplication.translate("ChatWindow", u"Display name of user", None))
#endif // QT_CONFIG(tooltip)
        self.usernameLine.setText(QCoreApplication.translate("ChatWindow", u"You", None))
        self.usernameLine.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"You", None))
#if QT_CONFIG(tooltip)
        self.customSysPromptText.setToolTip(QCoreApplication.translate("ChatWindow", u"Custom system prompt text", None))
#endif // QT_CONFIG(tooltip)
        self.customSysPromptText.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"Custom system prompt", None))
#if QT_CONFIG(tooltip)
        self.streamCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Streaming of text", None))
#endif // QT_CONFIG(tooltip)
        self.streamCheck.setText(QCoreApplication.translate("ChatWindow", u"Stream", None))
#if QT_CONFIG(tooltip)
        self.cacheCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Store context in cache", None))
#endif // QT_CONFIG(tooltip)
        self.cacheCheck.setText(QCoreApplication.translate("ChatWindow", u"Cache", None))
        self.label_12.setText(QCoreApplication.translate("ChatWindow", u"Bot name:", None))
        self.label_10.setText(QCoreApplication.translate("ChatWindow", u"User name:", None))
        self.groupBox.setTitle(QCoreApplication.translate("ChatWindow", u"Backend", None))
#if QT_CONFIG(tooltip)
        self.backendCppCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Use LLaMA.cpp server backend", None))
#endif // QT_CONFIG(tooltip)
        self.backendCppCheck.setText(QCoreApplication.translate("ChatWindow", u"LLaMA.cpp", None))
#if QT_CONFIG(tooltip)
        self.backendExllamaCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Use ExLLaMA V2 websockets server backend", None))
#endif // QT_CONFIG(tooltip)
        self.backendExllamaCheck.setText(QCoreApplication.translate("ChatWindow", u"ExLLaMA V2", None))
        self.rightToolbox.setItemText(self.rightToolbox.indexOf(self.preferencesPage), QCoreApplication.translate("ChatWindow", u"Preferences", None))
#if QT_CONFIG(tooltip)
        self.custStopStringLine.setToolTip(QCoreApplication.translate("ChatWindow", u"Comma separated list", None))
#endif // QT_CONFIG(tooltip)
        self.custStopStringLine.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"User, Bot", None))
#if QT_CONFIG(tooltip)
        self.stopStringAutoCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Auto add stop strings", None))
#endif // QT_CONFIG(tooltip)
        self.stopStringAutoCheck.setText(QCoreApplication.translate("ChatWindow", u"Auto add stop strings", None))
        self.label_13.setText(QCoreApplication.translate("ChatWindow", u"LLaVA image:", None))
#if QT_CONFIG(tooltip)
        self.penaliseNlCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Penalise newline tokens when applying the repeat penalty ", None))
#endif // QT_CONFIG(tooltip)
        self.penaliseNlCheck.setText(QCoreApplication.translate("ChatWindow", u"Penalise newlines", None))
        self.label_16.setText(QCoreApplication.translate("ChatWindow", u"Custom stop strings:", None))
#if QT_CONFIG(tooltip)
        self.autoSaveSessionCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Auto save session to file after generation", None))
#endif // QT_CONFIG(tooltip)
        self.autoSaveSessionCheck.setText(QCoreApplication.translate("ChatWindow", u"Auto save session", None))
#if QT_CONFIG(tooltip)
        self.imgFileLine.setToolTip(QCoreApplication.translate("ChatWindow", u"Image for LLaVA (llama.cpp only)", None))
#endif // QT_CONFIG(tooltip)
        self.imgFileLine.setText("")
        self.imgFileLine.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"Path to image for LLaVA usage", None))
#if QT_CONFIG(tooltip)
        self.autoscrollCheck.setToolTip(QCoreApplication.translate("ChatWindow", u"Autoscroll the output text when generating", None))
#endif // QT_CONFIG(tooltip)
        self.autoscrollCheck.setText(QCoreApplication.translate("ChatWindow", u"Autoscroll", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ChatWindow", u"Theme", None))
        self.themeNativeRadio.setText(QCoreApplication.translate("ChatWindow", u"Native", None))
        self.themeDarkRadio.setText(QCoreApplication.translate("ChatWindow", u"Dark", None))
        self.themeLightRadio.setText(QCoreApplication.translate("ChatWindow", u"Light", None))
        self.imgFileButton.setText(QCoreApplication.translate("ChatWindow", u"...", None))
        self.rightToolbox.setItemText(self.rightToolbox.indexOf(self.themesPage), QCoreApplication.translate("ChatWindow", u"Preferences - More", None))
#if QT_CONFIG(tooltip)
        self.clearButton.setToolTip(QCoreApplication.translate("ChatWindow", u"Clear the output history", None))
#endif // QT_CONFIG(tooltip)
        self.clearButton.setText(QCoreApplication.translate("ChatWindow", u"Clr", None))
#if QT_CONFIG(tooltip)
        self.generateButton.setToolTip(QCoreApplication.translate("ChatWindow", u"Start generation", None))
#endif // QT_CONFIG(tooltip)
        self.generateButton.setText(QCoreApplication.translate("ChatWindow", u"Gen", None))
#if QT_CONFIG(tooltip)
        self.continueButton.setToolTip(QCoreApplication.translate("ChatWindow", u"Rewinds the chat 1 turn", None))
#endif // QT_CONFIG(tooltip)
        self.continueButton.setText(QCoreApplication.translate("ChatWindow", u"Con", None))
#if QT_CONFIG(tooltip)
        self.rewindButton.setToolTip(QCoreApplication.translate("ChatWindow", u"Continue the last generation", None))
#endif // QT_CONFIG(tooltip)
        self.rewindButton.setText(QCoreApplication.translate("ChatWindow", u"Rw", None))
#if QT_CONFIG(tooltip)
        self.stopButton.setToolTip(QCoreApplication.translate("ChatWindow", u"Stop generation", None))
#endif // QT_CONFIG(tooltip)
        self.stopButton.setText(QCoreApplication.translate("ChatWindow", u"St", None))
        self.menuFile.setTitle(QCoreApplication.translate("ChatWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("ChatWindow", u"Help", None))
        self.menuEditors.setTitle(QCoreApplication.translate("ChatWindow", u"Editors", None))
    # retranslateUi

