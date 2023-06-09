import sys
import typing
from PyQt6 import QtCore, QtGui
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView, 
    QWidget, 
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel,QStandardItem, QPalette, QColor

REM = 16

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
    
        
        
class PrevCsvSelection(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QFormLayout(self)
        main_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.__track_name_label = QLabel()
        self.__artist_name_label = QLabel()
        self.__popularity_label = QLabel()
        self.__duration_label = QLabel()
        self.__obt_label = QLabel()
        self.__genre = QLabel() 
        main_layout.addRow('Nombre: ',self.__track_name_label)
        main_layout.addRow('Artista: ',self.__artist_name_label)
        main_layout.addRow('Popularidad: ',self.__popularity_label)
        main_layout.addRow('Duration: ',self.__duration_label)
        main_layout.addRow('Fecha de Lanzamiento: ',self.__obt_label)
        main_layout.addRow('Genero: ',self.__genre)
        
        self.setMinimumSize(300,100)
    
    
        
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Song Recomended')
        #self.setMinimumSize(1200,800)
        #Widgets
        self.__seeker = QLineEdit()
        self.__seeker.setPlaceholderText('Input song')
        self.__find_button = QPushButton('Search')
        csv_viewer = CSVViewer(df)
        
        #WidgetWindow Right
        self.__right_window_widget = QWidget()
        right_layout = QVBoxLayout()
        
        self.__generate_list_button = QPushButton('Generate List')
        self.__prev_csv_selection = PrevCsvSelection()
        
        right_layout.addStretch()
        right_layout.addWidget(self.__prev_csv_selection)
        right_layout.addWidget(self.__generate_list_button)
        right_layout.addStretch()
        right_layout.setSpacing(REM)
        #Layouts
        principal_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        search_section_layout = QHBoxLayout()
        principal_layout.setSpacing(REM)
        
        left_layout.addLayout(search_section_layout)
        
        
        
        principal_layout.addLayout(left_layout)
        principal_layout.addLayout(right_layout)

        search_section_layout.addWidget(self.__seeker)
        search_section_layout.addWidget(self.__find_button)
        left_layout.addWidget(csv_viewer)
        
        
        background = QWidget()
        background.setLayout(principal_layout)
        self.setCentralWidget(background)
    
    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(1200,900)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
