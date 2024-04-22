import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QProgressBar, QVBoxLayout, QWidget, QDialog



class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Выполнение операции")
        self.resize(600, 100)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def updateProgress(self,value):
        if value >= 100:
            self.progress_bar.setValue(0)
            self.close()
        else:
            self.progress_bar.setValue(value)


    def closeEvent(self, event):
        super().closeEvent(event)
