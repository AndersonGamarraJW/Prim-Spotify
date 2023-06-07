import sys
import typing
import pandas as pd
from PyQt6.QtWidgets import QApplication,QMainWindow,QTableView, QWidget, QHBoxLayout,QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel,QStandardItem


df = pd.read_csv('music_genre.csv')
         
class CSVViewer(QTableView):
    def __init__(self,data):
        super().__init__()
        model = QStandardItemModel()
        model.setColumnCount(len(data.columns))
        model.setHorizontalHeaderLabels(data.columns)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                item = QStandardItem(str(data.iloc[row,col]))
                model.setItem(row,col,item)
        
        self.setModel(model)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        
        self.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.setHorizontalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
         
        
         
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Song Recomended')
        self.setMinimumSize(1200,800)
        principal_layout = QHBoxLayout()
        #csv_viewer = QWidget()
        csv_viewer = CSVViewer(df)
        principal_layout.addWidget(csv_viewer)
        prev_csv_viewer = QWidget()
        principal_layout.addWidget(prev_csv_viewer)
        background = QWidget()
        background.setLayout(principal_layout)
        self.setCentralWidget(background)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
