import sys
import os
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
    QStyleOption,
    QStyle,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QPainter,
    QColor
)

REM = 16

df = pd.read_csv('music_genre.csv')

class MainPalletColor:
    BLACK = '#222831'
    PRINCIPAL = '#DDDDDD'
    CONTRAST = '#F05454'
    LIGHT = '#EEEEEE'
    SHADOW = '#ababab'
    INTENSE_SHADOW = '#696969'

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

        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setObjectName('csv-viewer')

        self.setShowGrid(False)
        #Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(MainPalletColor.SHADOW))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow) 
        
class PrevCsvSelection(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QFormLayout(self)
        main_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        
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
        
        
        self.setObjectName('csv-selection')
        
        # Crear el efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(MainPalletColor.SHADOW))
        shadow.setOffset(0, 0)

        # Aplicar el efecto de sombra al widget
        self.setGraphicsEffect(shadow)

        self.setMinimumSize(225,400)
     
    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget,o,painter,self)
        
        

class CustomButton(QPushButton):
    def __init__(self,text,objectName=None):
        super().__init__(text=text)
        if objectName != None:
            self.setObjectName(objectName)
        
        self.setMaximumSize(150,200)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(MainPalletColor.SHADOW))
        shadow.setOffset(0,0)
        self.setGraphicsEffect(shadow)
          
    def sizeHint(self) -> QSize:
        return QSize(150,30)    
    
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
        
        #Generate List Button
        self.__generate_list_button = CustomButton('Generate List','generate-list-button')
        
        self.__prev_csv_selection = PrevCsvSelection()
        
        right_layout.addStretch()
        right_layout.addWidget(self.__prev_csv_selection)
        right_layout.addWidget(self.__generate_list_button,alignment=Qt.AlignmentFlag.AlignCenter)
        right_layout.addStretch()
        right_layout.setSpacing(2*REM)
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
    file_path = os.path.abspath(__file__)
    dir_file_path = os.path.dirname(file_path)
    style_path = os.path.join(dir_file_path,'style.css')
    with open(style_path,'r') as f:
        style = f.read()
    app.setStyleSheet(style)
    main_window = MainWindow()
    main_window.show()
    app.exec()
