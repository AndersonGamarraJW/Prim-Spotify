import sys
import typing
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView, 
    QWidget, 
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel,QStandardItem


df = pd.read_csv('music_genre.csv')
         
class CSVViewer(QTableView):
    def __init__(self,data):
        super().__init__()
        model = QStandardItemModel()
        column_names = ['track_name'] #Columnas que se desean mostrar
        
        model.setColumnCount(len(column_names))
        model.setHorizontalHeaderLabels(column_names)
        for row in range(data.shape[0]):
            item = QStandardItem(str(data.at[row,'track_name']))
            model.setItem(row,0,item)
    
        
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
        #Widgets
        self.__seeker = QLineEdit()
        self.__seeker.setPlaceholderText('Input song')
        
        self.__find_button = QPushButton('Search')
        self.__generate_list_button = QPushButton('Generate List')
        csv_viewer = CSVViewer(df)
        
        
        #Layouts
        principal_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        search_section_layout = QHBoxLayout()
        
        
        left_layout.addLayout(search_section_layout)
        
        principal_layout.addLayout(left_layout)
        principal_layout.addLayout(right_layout)

        search_section_layout.addWidget(self.__seeker)
        search_section_layout.addWidget(self.__find_button)
        left_layout.addWidget(csv_viewer)
        right_layout.addWidget(self.__generate_list_button)
        
        background = QWidget()
        background.setLayout(principal_layout)
        self.setCentralWidget(background)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
