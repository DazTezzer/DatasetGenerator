# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(838, 537)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(100, 100))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.globalExceptionHandlerPlainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.globalExceptionHandlerPlainTextEdit.sizePolicy().hasHeightForWidth())
        self.globalExceptionHandlerPlainTextEdit.setSizePolicy(sizePolicy)
        self.globalExceptionHandlerPlainTextEdit.setObjectName("globalExceptionHandlerPlainTextEdit")
        self.gridLayout.addWidget(self.globalExceptionHandlerPlainTextEdit, 2, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(100, 100))
        self.tabWidget.setObjectName("tabWidget")
        self.generatorTab = QtWidgets.QWidget()
        self.generatorTab.setObjectName("generatorTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.generatorTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.areaListView = QtWidgets.QListView(self.generatorTab)
        self.areaListView.setMaximumSize(QtCore.QSize(500, 500))
        self.areaListView.setObjectName("areaListView")
        self.verticalLayout.addWidget(self.areaListView)
        self.areaFileDialogButton = QtWidgets.QPushButton(self.generatorTab)
        self.areaFileDialogButton.setMaximumSize(QtCore.QSize(500, 500))
        self.areaFileDialogButton.setObjectName("areaFileDialogButton")
        self.verticalLayout.addWidget(self.areaFileDialogButton)
        self.objectListView = QtWidgets.QListView(self.generatorTab)
        self.objectListView.setMaximumSize(QtCore.QSize(500, 500))
        self.objectListView.setObjectName("objectListView")
        self.verticalLayout.addWidget(self.objectListView)
        self.objectFileDialogButton = QtWidgets.QPushButton(self.generatorTab)
        self.objectFileDialogButton.setMaximumSize(QtCore.QSize(500, 500))
        self.objectFileDialogButton.setObjectName("objectFileDialogButton")
        self.verticalLayout.addWidget(self.objectFileDialogButton)
        self.line = QtWidgets.QFrame(self.generatorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.dataGenerateButton = QtWidgets.QPushButton(self.generatorTab)
        self.dataGenerateButton.setObjectName("dataGenerateButton")
        self.verticalLayout.addWidget(self.dataGenerateButton)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 2, 1)
        self.areaGraphicsView = QtWidgets.QGraphicsView(self.generatorTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.areaGraphicsView.sizePolicy().hasHeightForWidth())
        self.areaGraphicsView.setSizePolicy(sizePolicy)
        self.areaGraphicsView.setMinimumSize(QtCore.QSize(500, 0))
        self.areaGraphicsView.setObjectName("areaGraphicsView")
        self.gridLayout_2.addWidget(self.areaGraphicsView, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.saveOverlayButton = QtWidgets.QPushButton(self.generatorTab)
        self.saveOverlayButton.setObjectName("saveOverlayButton")
        self.horizontalLayout_2.addWidget(self.saveOverlayButton)
        self.deleteOverlayButton = QtWidgets.QPushButton(self.generatorTab)
        self.deleteOverlayButton.setObjectName("deleteOverlayButton")
        self.horizontalLayout_2.addWidget(self.deleteOverlayButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.tabWidget.addTab(self.generatorTab, "")
        self.trainingTab = QtWidgets.QWidget()
        self.trainingTab.setObjectName("trainingTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.trainingTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.datasetListUpdateButton = QtWidgets.QPushButton(self.trainingTab)
        self.datasetListUpdateButton.setObjectName("datasetListUpdateButton")
        self.verticalLayout_2.addWidget(self.datasetListUpdateButton)
        self.datasetListView = QtWidgets.QListView(self.trainingTab)
        self.datasetListView.setObjectName("datasetListView")
        self.verticalLayout_2.addWidget(self.datasetListView)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.modelStartTrainingButton = QtWidgets.QPushButton(self.trainingTab)
        self.modelStartTrainingButton.setObjectName("modelStartTrainingButton")
        self.gridLayout_3.addWidget(self.modelStartTrainingButton, 1, 0, 1, 1)
        self.tabWidget.addTab(self.trainingTab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 838, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.areaFileDialogButton.setText(_translate("MainWindow", "Выбрать папку с исходными изображениями"))
        self.objectFileDialogButton.setText(_translate("MainWindow", "Выбрать папку с изображениями объектов"))
        self.dataGenerateButton.setText(_translate("MainWindow", "Собрать датасет"))
        self.saveOverlayButton.setText(_translate("MainWindow", "Сохранить разметку"))
        self.deleteOverlayButton.setText(_translate("MainWindow", "Удалить разметку"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generatorTab), _translate("MainWindow", "Генератор Датасета"))
        self.datasetListUpdateButton.setText(_translate("MainWindow", "Обновить список датасетов"))
        self.modelStartTrainingButton.setText(_translate("MainWindow", "Обучить модель"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trainingTab), _translate("MainWindow", "Обучение модели"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Тестирование модели"))
