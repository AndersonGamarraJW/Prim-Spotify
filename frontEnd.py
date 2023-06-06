import sys
from PyQt6.QtWidgets import QApplication,QMainWindow,QTableView, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel,QStandardItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Song Recomended')
        self.setMinimumSize(1200,800)
        principal_layout = QHBoxLayout()
        
        background = QWidget()
        background.setLayout(principal_layout)
        self.setCentralWidget(background)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
    