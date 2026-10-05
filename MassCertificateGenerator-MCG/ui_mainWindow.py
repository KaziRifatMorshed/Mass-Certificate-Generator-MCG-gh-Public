# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QSplitter, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)
import resourcs_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1186, 849)
        icon = QIcon()
        icon.addFile(u":/logo/extra/MCG_logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pipeline_tabWidget = QTabWidget(self.layoutWidget)
        self.pipeline_tabWidget.setObjectName(u"pipeline_tabWidget")
        self.pipeline_tabWidget.setMinimumSize(QSize(50, 50))
        self.pipeline_tabWidget.setTabBarAutoHide(False)
        self.ConfigTab = QWidget()
        self.ConfigTab.setObjectName(u"ConfigTab")
        self.formLayout = QFormLayout(self.ConfigTab)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.ConfigTab)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.templateFilePath_label = QLabel(self.ConfigTab)
        self.templateFilePath_label.setObjectName(u"templateFilePath_label")
        sizePolicy.setHeightForWidth(self.templateFilePath_label.sizePolicy().hasHeightForWidth())
        self.templateFilePath_label.setSizePolicy(sizePolicy)
        self.templateFilePath_label.setWordWrap(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.templateFilePath_label)

        self.label_28 = QLabel(self.ConfigTab)
        self.label_28.setObjectName(u"label_28")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_28)

        self.selectTemplate_pushButton = QPushButton(self.ConfigTab)
        self.selectTemplate_pushButton.setObjectName(u"selectTemplate_pushButton")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.selectTemplate_pushButton)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(2, QFormLayout.ItemRole.FieldRole, self.verticalSpacer_3)

        self.pipeline_tabWidget.addTab(self.ConfigTab, "")
        self.fontTab = QWidget()
        self.fontTab.setObjectName(u"fontTab")
        self.verticalLayout_4 = QVBoxLayout(self.fontTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.addNewFont_newGrpBox_pushButton = QPushButton(self.fontTab)
        self.addNewFont_newGrpBox_pushButton.setObjectName(u"addNewFont_newGrpBox_pushButton")

        self.verticalLayout_4.addWidget(self.addNewFont_newGrpBox_pushButton)

        self.verticalSpacer = QSpacerItem(20, 98, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.font_groupBox = QGroupBox(self.fontTab)
        self.font_groupBox.setObjectName(u"font_groupBox")
        self.formLayout_3 = QFormLayout(self.font_groupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_4 = QLabel(self.font_groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.fontName_lineEdit = QLineEdit(self.font_groupBox)
        self.fontName_lineEdit.setObjectName(u"fontName_lineEdit")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.fontName_lineEdit)

        self.thisFontLocation_label = QLabel(self.font_groupBox)
        self.thisFontLocation_label.setObjectName(u"thisFontLocation_label")
        sizePolicy.setHeightForWidth(self.thisFontLocation_label.sizePolicy().hasHeightForWidth())
        self.thisFontLocation_label.setSizePolicy(sizePolicy)
        self.thisFontLocation_label.setWordWrap(True)

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.thisFontLocation_label)

        self.label_5 = QLabel(self.font_groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.selectFontFile_pushButton = QPushButton(self.font_groupBox)
        self.selectFontFile_pushButton.setObjectName(u"selectFontFile_pushButton")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.selectFontFile_pushButton)

        self.deleteCorrntFont_pushButton = QPushButton(self.font_groupBox)
        self.deleteCorrntFont_pushButton.setObjectName(u"deleteCorrntFont_pushButton")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.deleteCorrntFont_pushButton)


        self.verticalLayout_4.addWidget(self.font_groupBox)

        self.pipeline_tabWidget.addTab(self.fontTab, "")
        self.importDataTab = QWidget()
        self.importDataTab.setObjectName(u"importDataTab")
        self.verticalLayout_5 = QVBoxLayout(self.importDataTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.imortData_groupBox = QGroupBox(self.importDataTab)
        self.imortData_groupBox.setObjectName(u"imortData_groupBox")
        self.formLayout_4 = QFormLayout(self.imortData_groupBox)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_6 = QLabel(self.imortData_groupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.importFileFotmat_comboBox = QComboBox(self.imortData_groupBox)
        self.importFileFotmat_comboBox.addItem("")
        self.importFileFotmat_comboBox.addItem("")
        self.importFileFotmat_comboBox.setObjectName(u"importFileFotmat_comboBox")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.importFileFotmat_comboBox)

        self.label_7 = QLabel(self.imortData_groupBox)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.imoportFilePath_label = QLabel(self.imortData_groupBox)
        self.imoportFilePath_label.setObjectName(u"imoportFilePath_label")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.imoportFilePath_label)

        self.selectImortFile_pushButton = QPushButton(self.imortData_groupBox)
        self.selectImortFile_pushButton.setObjectName(u"selectImortFile_pushButton")

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.FieldRole, self.selectImortFile_pushButton)

        self.label_8 = QLabel(self.imortData_groupBox)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_4.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.label_9 = QLabel(self.imortData_groupBox)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_4.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.importFiile_columHeaders_label = QLabel(self.imortData_groupBox)
        self.importFiile_columHeaders_label.setObjectName(u"importFiile_columHeaders_label")
        font1 = QFont()
        font1.setPointSize(11)
        self.importFiile_columHeaders_label.setFont(font1)
        self.importFiile_columHeaders_label.setWordWrap(True)

        self.formLayout_4.setWidget(3, QFormLayout.ItemRole.FieldRole, self.importFiile_columHeaders_label)


        self.verticalLayout_5.addWidget(self.imortData_groupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 137, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.pipeline_tabWidget.addTab(self.importDataTab, "")
        self.textBodyTab = QWidget()
        self.textBodyTab.setObjectName(u"textBodyTab")
        self.verticalLayout_6 = QVBoxLayout(self.textBodyTab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.addNewText_pushButton = QPushButton(self.textBodyTab)
        self.addNewText_pushButton.setObjectName(u"addNewText_pushButton")

        self.verticalLayout_6.addWidget(self.addNewText_pushButton)

        self.TEXT_groupBox = QGroupBox(self.textBodyTab)
        self.TEXT_groupBox.setObjectName(u"TEXT_groupBox")
        self.gridLayout = QGridLayout(self.TEXT_groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_3 = QFrame(self.TEXT_groupBox)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_3, 3, 2, 1, 1)

        self.line_2 = QFrame(self.TEXT_groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 3, 7, 1, 1)

        self.isUndrline_checkBox = QCheckBox(self.TEXT_groupBox)
        self.isUndrline_checkBox.setObjectName(u"isUndrline_checkBox")

        self.gridLayout.addWidget(self.isUndrline_checkBox, 3, 5, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.variable_or_constant_comboBox = QComboBox(self.TEXT_groupBox)
        self.variable_or_constant_comboBox.addItem("")
        self.variable_or_constant_comboBox.addItem("")
        self.variable_or_constant_comboBox.setObjectName(u"variable_or_constant_comboBox")

        self.horizontalLayout_3.addWidget(self.variable_or_constant_comboBox)

        self.selectVariables_comboBox = QComboBox(self.TEXT_groupBox)
        self.selectVariables_comboBox.setObjectName(u"selectVariables_comboBox")

        self.horizontalLayout_3.addWidget(self.selectVariables_comboBox)

        self.horizontalLayout_3.setStretch(1, 1)

        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 10)

        self.selectFontForCurrentText_comboBox = QComboBox(self.TEXT_groupBox)
        self.selectFontForCurrentText_comboBox.setObjectName(u"selectFontForCurrentText_comboBox")

        self.gridLayout.addWidget(self.selectFontForCurrentText_comboBox, 4, 1, 1, 4)

        self.label_17 = QLabel(self.TEXT_groupBox)
        self.label_17.setObjectName(u"label_17")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_17, 3, 0, 1, 1)

        self.textSize_spinBox = QSpinBox(self.TEXT_groupBox)
        self.textSize_spinBox.setObjectName(u"textSize_spinBox")
        self.textSize_spinBox.setMinimum(1)
        self.textSize_spinBox.setMaximum(999)
        self.textSize_spinBox.setValue(12)

        self.gridLayout.addWidget(self.textSize_spinBox, 3, 1, 1, 1)

        self.constantText_plainTextEdit = QPlainTextEdit(self.TEXT_groupBox)
        self.constantText_plainTextEdit.setObjectName(u"constantText_plainTextEdit")
        self.constantText_plainTextEdit.setMinimumSize(QSize(0, 50))
        self.constantText_plainTextEdit.setMaximumSize(QSize(16777215, 70))

        self.gridLayout.addWidget(self.constantText_plainTextEdit, 1, 0, 1, 10)

        self.sendUp_pushButton = QPushButton(self.TEXT_groupBox)
        self.sendUp_pushButton.setObjectName(u"sendUp_pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sendUp_pushButton.sizePolicy().hasHeightForWidth())
        self.sendUp_pushButton.setSizePolicy(sizePolicy2)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.sendUp_pushButton.setIcon(icon1)

        self.gridLayout.addWidget(self.sendUp_pushButton, 0, 11, 2, 1)

        self.isItalic_checkBox = QCheckBox(self.TEXT_groupBox)
        self.isItalic_checkBox.setObjectName(u"isItalic_checkBox")

        self.gridLayout.addWidget(self.isItalic_checkBox, 3, 4, 1, 1)

        self.isBold_checkBox = QCheckBox(self.TEXT_groupBox)
        self.isBold_checkBox.setObjectName(u"isBold_checkBox")

        self.gridLayout.addWidget(self.isBold_checkBox, 3, 3, 1, 1)

        self.label_19 = QLabel(self.TEXT_groupBox)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout.addWidget(self.label_19, 4, 0, 1, 1)

        self.isNewlineAtEnd_checkBox = QCheckBox(self.TEXT_groupBox)
        self.isNewlineAtEnd_checkBox.setObjectName(u"isNewlineAtEnd_checkBox")

        self.gridLayout.addWidget(self.isNewlineAtEnd_checkBox, 3, 6, 1, 1)

        self.currentTextColor_pushButton = QPushButton(self.TEXT_groupBox)
        self.currentTextColor_pushButton.setObjectName(u"currentTextColor_pushButton")

        self.gridLayout.addWidget(self.currentTextColor_pushButton, 4, 5, 1, 2)

        self.deleteCurrentText_pushButton = QPushButton(self.TEXT_groupBox)
        self.deleteCurrentText_pushButton.setObjectName(u"deleteCurrentText_pushButton")

        self.gridLayout.addWidget(self.deleteCurrentText_pushButton, 4, 7, 1, 3)

        self.sendDown_pushButton = QPushButton(self.TEXT_groupBox)
        self.sendDown_pushButton.setObjectName(u"sendDown_pushButton")
        sizePolicy2.setHeightForWidth(self.sendDown_pushButton.sizePolicy().hasHeightForWidth())
        self.sendDown_pushButton.setSizePolicy(sizePolicy2)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoDown))
        self.sendDown_pushButton.setIcon(icon2)

        self.gridLayout.addWidget(self.sendDown_pushButton, 2, 11, 3, 1)

        self.line = QFrame(self.TEXT_groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 0, 10, 5, 1)


        self.verticalLayout_6.addWidget(self.TEXT_groupBox)

        self.verticalSpacer_5 = QSpacerItem(20, 262, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_5)

        self.pipeline_tabWidget.addTab(self.textBodyTab, "")
        self.exportTab = QWidget()
        self.exportTab.setObjectName(u"exportTab")
        self.formLayout_5 = QFormLayout(self.exportTab)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label_10 = QLabel(self.exportTab)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_10)

        self.exportFolderLocaion_label = QLabel(self.exportTab)
        self.exportFolderLocaion_label.setObjectName(u"exportFolderLocaion_label")
        self.exportFolderLocaion_label.setWordWrap(True)

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.FieldRole, self.exportFolderLocaion_label)

        self.label_11 = QLabel(self.exportTab)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.selectExportLocation_pushButton = QPushButton(self.exportTab)
        self.selectExportLocation_pushButton.setObjectName(u"selectExportLocation_pushButton")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.FieldRole, self.selectExportLocation_pushButton)

        self.label_12 = QLabel(self.exportTab)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_12)

        self.singleFile_multipleFiile_comboBox = QComboBox(self.exportTab)
        self.singleFile_multipleFiile_comboBox.addItem("")
        self.singleFile_multipleFiile_comboBox.addItem("")
        self.singleFile_multipleFiile_comboBox.setObjectName(u"singleFile_multipleFiile_comboBox")

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.FieldRole, self.singleFile_multipleFiile_comboBox)

        self.EXPORT_pushButton = QPushButton(self.exportTab)
        self.EXPORT_pushButton.setObjectName(u"EXPORT_pushButton")
        font2 = QFont()
        font2.setPointSize(14)
        self.EXPORT_pushButton.setFont(font2)

        self.formLayout_5.setWidget(6, QFormLayout.ItemRole.FieldRole, self.EXPORT_pushButton)

        self.label_13 = QLabel(self.exportTab)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_5.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_13)

        self.label_14 = QLabel(self.exportTab)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setWordWrap(True)

        self.formLayout_5.setWidget(4, QFormLayout.ItemRole.FieldRole, self.label_14)

        self.label_15 = QLabel(self.exportTab)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_5.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_15)

        self.label_16 = QLabel(self.exportTab)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_5.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_16)

        self.oututFiileNameField_comboBox = QComboBox(self.exportTab)
        self.oututFiileNameField_comboBox.setObjectName(u"oututFiileNameField_comboBox")

        self.formLayout_5.setWidget(3, QFormLayout.ItemRole.FieldRole, self.oututFiileNameField_comboBox)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout_5.setItem(7, QFormLayout.ItemRole.FieldRole, self.verticalSpacer_4)

        self.label_27 = QLabel(self.exportTab)
        self.label_27.setObjectName(u"label_27")

        self.formLayout_5.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_27)

        self.outputFormat_comboBox = QComboBox(self.exportTab)
        self.outputFormat_comboBox.addItem("")
        self.outputFormat_comboBox.addItem("")
        self.outputFormat_comboBox.addItem("")
        self.outputFormat_comboBox.setObjectName(u"outputFormat_comboBox")

        self.formLayout_5.setWidget(5, QFormLayout.ItemRole.FieldRole, self.outputFormat_comboBox)

        self.pipeline_tabWidget.addTab(self.exportTab, "")

        self.verticalLayout.addWidget(self.pipeline_tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.prevTab_pushButton = QPushButton(self.layoutWidget)
        self.prevTab_pushButton.setObjectName(u"prevTab_pushButton")

        self.horizontalLayout_2.addWidget(self.prevTab_pushButton)

        self.nextTab_pushButton = QPushButton(self.layoutWidget)
        self.nextTab_pushButton.setObjectName(u"nextTab_pushButton")

        self.horizontalLayout_2.addWidget(self.nextTab_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.layoutWidget)
        self.preview_groupBox = QGroupBox(self.splitter)
        self.preview_groupBox.setObjectName(u"preview_groupBox")
        self.preview_groupBox.setMinimumSize(QSize(50, 50))
        self.verticalLayout_7 = QVBoxLayout(self.preview_groupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_3 = QLabel(self.preview_groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.debuggingMode_checkBox = QCheckBox(self.preview_groupBox)
        self.debuggingMode_checkBox.setObjectName(u"debuggingMode_checkBox")
        self.debuggingMode_checkBox.setEnabled(True)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.debuggingMode_checkBox)


        self.verticalLayout_7.addLayout(self.formLayout_2)

        self.textBoxCoordinate_groupBox = QGroupBox(self.preview_groupBox)
        self.textBoxCoordinate_groupBox.setObjectName(u"textBoxCoordinate_groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.textBoxCoordinate_groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_20 = QLabel(self.textBoxCoordinate_groupBox)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_20)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_21 = QLabel(self.textBoxCoordinate_groupBox)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_3.addWidget(self.label_21, 0, 0, 1, 2)

        self.line_4 = QFrame(self.textBoxCoordinate_groupBox)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_3.addWidget(self.line_4, 0, 2, 4, 1)

        self.label_24 = QLabel(self.textBoxCoordinate_groupBox)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_3.addWidget(self.label_24, 0, 3, 1, 2)

        self.label_25 = QLabel(self.textBoxCoordinate_groupBox)
        self.label_25.setObjectName(u"label_25")
        sizePolicy1.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.label_25, 1, 0, 1, 1)

        self.topLeft_x_spinBox = QSpinBox(self.textBoxCoordinate_groupBox)
        self.topLeft_x_spinBox.setObjectName(u"topLeft_x_spinBox")

        self.gridLayout_3.addWidget(self.topLeft_x_spinBox, 1, 1, 2, 1)

        self.label_26 = QLabel(self.textBoxCoordinate_groupBox)
        self.label_26.setObjectName(u"label_26")
        sizePolicy1.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.label_26, 1, 3, 1, 1)

        self.bottomRight_x_spinBox = QSpinBox(self.textBoxCoordinate_groupBox)
        self.bottomRight_x_spinBox.setObjectName(u"bottomRight_x_spinBox")

        self.gridLayout_3.addWidget(self.bottomRight_x_spinBox, 1, 4, 1, 1)

        self.label_23 = QLabel(self.textBoxCoordinate_groupBox)
        self.label_23.setObjectName(u"label_23")
        sizePolicy1.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.label_23, 2, 3, 2, 1)

        self.label_22 = QLabel(self.textBoxCoordinate_groupBox)
        self.label_22.setObjectName(u"label_22")
        sizePolicy1.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.label_22, 3, 0, 1, 1)

        self.topLeft_y_spinBox = QSpinBox(self.textBoxCoordinate_groupBox)
        self.topLeft_y_spinBox.setObjectName(u"topLeft_y_spinBox")

        self.gridLayout_3.addWidget(self.topLeft_y_spinBox, 3, 1, 1, 1)

        self.bottomRight_y_spinBox = QSpinBox(self.textBoxCoordinate_groupBox)
        self.bottomRight_y_spinBox.setObjectName(u"bottomRight_y_spinBox")

        self.gridLayout_3.addWidget(self.bottomRight_y_spinBox, 3, 4, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_18 = QLabel(self.textBoxCoordinate_groupBox)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_4.addWidget(self.label_18)

        self.currentTextAlignment_comboBox = QComboBox(self.textBoxCoordinate_groupBox)
        self.currentTextAlignment_comboBox.addItem("")
        self.currentTextAlignment_comboBox.addItem("")
        self.currentTextAlignment_comboBox.addItem("")
        self.currentTextAlignment_comboBox.addItem("")
        self.currentTextAlignment_comboBox.setObjectName(u"currentTextAlignment_comboBox")

        self.horizontalLayout_4.addWidget(self.currentTextAlignment_comboBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_7.addWidget(self.textBoxCoordinate_groupBox)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.left_top_x_horizontalSlider = QSlider(self.preview_groupBox)
        self.left_top_x_horizontalSlider.setObjectName(u"left_top_x_horizontalSlider")
        self.left_top_x_horizontalSlider.setMaximum(100)
        self.left_top_x_horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout_2.addWidget(self.left_top_x_horizontalSlider, 0, 1, 1, 1)

        self.left_top_y_verticalSlider = QSlider(self.preview_groupBox)
        self.left_top_y_verticalSlider.setObjectName(u"left_top_y_verticalSlider")
        self.left_top_y_verticalSlider.setMaximum(100)
        self.left_top_y_verticalSlider.setOrientation(Qt.Orientation.Vertical)
        self.left_top_y_verticalSlider.setInvertedAppearance(True)

        self.gridLayout_2.addWidget(self.left_top_y_verticalSlider, 1, 0, 1, 1)

        self.pdfThumbViwerWidget = QPdfView(self.preview_groupBox)
        self.pdfThumbViwerWidget.setObjectName(u"pdfThumbViwerWidget")

        self.gridLayout_2.addWidget(self.pdfThumbViwerWidget, 1, 1, 1, 1)

        self.botto_right_y_verticalSlider = QSlider(self.preview_groupBox)
        self.botto_right_y_verticalSlider.setObjectName(u"botto_right_y_verticalSlider")
        self.botto_right_y_verticalSlider.setMaximum(100)
        self.botto_right_y_verticalSlider.setOrientation(Qt.Orientation.Vertical)

        self.gridLayout_2.addWidget(self.botto_right_y_verticalSlider, 1, 2, 1, 1)

        self.bottom_right_x_horizontalSlider = QSlider(self.preview_groupBox)
        self.bottom_right_x_horizontalSlider.setObjectName(u"bottom_right_x_horizontalSlider")
        self.bottom_right_x_horizontalSlider.setMaximum(100)
        self.bottom_right_x_horizontalSlider.setValue(0)
        self.bottom_right_x_horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.bottom_right_x_horizontalSlider.setInvertedAppearance(True)
        self.bottom_right_x_horizontalSlider.setInvertedControls(False)

        self.gridLayout_2.addWidget(self.bottom_right_x_horizontalSlider, 2, 1, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout_2)

        self.splitter.addWidget(self.preview_groupBox)

        self.verticalLayout_2.addWidget(self.splitter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.exit_pushButton = QPushButton(self.centralwidget)
        self.exit_pushButton.setObjectName(u"exit_pushButton")
        sizePolicy1.setHeightForWidth(self.exit_pushButton.sizePolicy().hasHeightForWidth())
        self.exit_pushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.exit_pushButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_29 = QLabel(self.centralwidget)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.label_29)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.help_pushButton = QPushButton(self.centralwidget)
        self.help_pushButton.setObjectName(u"help_pushButton")
        sizePolicy1.setHeightForWidth(self.help_pushButton.sizePolicy().hasHeightForWidth())
        self.help_pushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.help_pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1186, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.exit_pushButton.clicked.connect(MainWindow.close)

        self.pipeline_tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mass Certificate Generator - MCG", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Mass Certificate Generator", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Select PDF template:", None))
        self.templateFilePath_label.setText(QCoreApplication.translate("MainWindow", u"No PDF selected", None))
        self.label_28.setText("")
        self.selectTemplate_pushButton.setText(QCoreApplication.translate("MainWindow", u"Select Template PDF File", None))
        self.pipeline_tabWidget.setTabText(self.pipeline_tabWidget.indexOf(self.ConfigTab), QCoreApplication.translate("MainWindow", u"Config", None))
        self.addNewFont_newGrpBox_pushButton.setText(QCoreApplication.translate("MainWindow", u"Add New Font", None))
        self.font_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Font: ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Font Name:", None))
        self.thisFontLocation_label.setText(QCoreApplication.translate("MainWindow", u"Not Selected", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Font File Location:", None))
        self.selectFontFile_pushButton.setText(QCoreApplication.translate("MainWindow", u"Select Font File", None))
        self.deleteCorrntFont_pushButton.setText(QCoreApplication.translate("MainWindow", u"Delete Font", None))
        self.pipeline_tabWidget.setTabText(self.pipeline_tabWidget.indexOf(self.fontTab), QCoreApplication.translate("MainWindow", u"Font", None))
        self.imortData_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Import data from file", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"File Format:", None))
        self.importFileFotmat_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"CSV", None))
        self.importFileFotmat_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Excel files (.xlsx)", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"File path:", None))
        self.imoportFilePath_label.setText(QCoreApplication.translate("MainWindow", u"No file Selected", None))
        self.selectImortFile_pushButton.setText(QCoreApplication.translate("MainWindow", u"Select File", None))
        self.label_8.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Fields:", None))
        self.importFiile_columHeaders_label.setText(QCoreApplication.translate("MainWindow", u"empty", None))
        self.pipeline_tabWidget.setTabText(self.pipeline_tabWidget.indexOf(self.importDataTab), QCoreApplication.translate("MainWindow", u"Import Data", None))
        self.addNewText_pushButton.setText(QCoreApplication.translate("MainWindow", u"Add New Text", None))
        self.TEXT_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Text No:", None))
        self.isUndrline_checkBox.setText(QCoreApplication.translate("MainWindow", u"Underline", None))
        self.variable_or_constant_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Variable", None))
        self.variable_or_constant_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Constant", None))

        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Size:", None))
        self.constantText_plainTextEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Write Text Here", None))
        self.sendUp_pushButton.setText(QCoreApplication.translate("MainWindow", u"Up", None))
        self.isItalic_checkBox.setText(QCoreApplication.translate("MainWindow", u"Italic", None))
        self.isBold_checkBox.setText(QCoreApplication.translate("MainWindow", u"Bold", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Font:", None))
        self.isNewlineAtEnd_checkBox.setText(QCoreApplication.translate("MainWindow", u"Line Break", None))
        self.currentTextColor_pushButton.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.deleteCurrentText_pushButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.sendDown_pushButton.setText(QCoreApplication.translate("MainWindow", u"Down", None))
        self.pipeline_tabWidget.setTabText(self.pipeline_tabWidget.indexOf(self.textBodyTab), QCoreApplication.translate("MainWindow", u"Text Body", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Export Folder Location:", None))
        self.exportFolderLocaion_label.setText(QCoreApplication.translate("MainWindow", u"Not Selected", None))
        self.label_11.setText("")
        self.selectExportLocation_pushButton.setText(QCoreApplication.translate("MainWindow", u"Select Export Location", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Config:", None))
        self.singleFile_multipleFiile_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Individul Files", None))
        self.singleFile_multipleFiile_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Single File", None))

        self.EXPORT_pushButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.label_13.setText("")
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Guide:</span></p><p><span style=\" font-weight:700;\">Individul Files: </span>One file will be generated based on the person name (or the field you set) for each person.</p><p><span style=\" font-weight:700;\">Single File:</span> One file will contain certificates of all individuals.</p></body></html>", None))
        self.label_15.setText("")
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"File Name:", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Output Format:", None))
        self.outputFormat_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"PDF", None))
        self.outputFormat_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"PNG", None))
        self.outputFormat_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"JPEG", None))

        self.pipeline_tabWidget.setTabText(self.pipeline_tabWidget.indexOf(self.exportTab), QCoreApplication.translate("MainWindow", u"Export", None))
        self.prevTab_pushButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.nextTab_pushButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.preview_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Preview", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Debugging Mode:", None))
        self.debuggingMode_checkBox.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.textBoxCoordinate_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Text Box Coordinate", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>What is Textbox ?</p><p>Textbox is a container where Text Body (what you want to write using this software) will be written. Use these coordinate values or use the slider below to resize your textbox.</p></body></html>", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Top Left", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Bottom Right", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"X:", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"X:", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Y:", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Y:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Text Alignment:", None))
        self.currentTextAlignment_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"CENTER", None))
        self.currentTextAlignment_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"LEFT", None))
        self.currentTextAlignment_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"RIGHT", None))
        self.currentTextAlignment_comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"JUSTIFY", None))

        self.exit_pushButton.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Website: <a href=\"https://kazirifatmorshed.github.io/projects/MassCertificateGenerator.html\"><span style=\" text-decoration: underline; color:#27bf73;\">https://kazirifatmorshed.github.io/projects/MassCertificateGenerator.html</span></a></p></body></html>", None))
        self.help_pushButton.setText(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

