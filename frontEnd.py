import sys
import os
from PyQt6 import QtCore, QtGui
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math 
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
    QGraphicsDropShadowEffect,
    QStyledItemDelegate,
    QStyleOptionViewItem
)
from PyQt6.QtCore import Qt,QSize,QEvent,QPropertyAnimation,QByteArray,QVariantAnimation,QEasingCurve, QTimer, QAbstractAnimation,QUrl
from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QPainter,
    QColor,
    QPalette,
    QPen,
    QBrush,
    QCursor,
    QPainterPath,
    QPixmap,
    QPolygon,
    QRegion,
    QBitmap,
    QIcon,
    QDesktopServices
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests


#Spotify API
CLIENT_ID = 'e089516fb6b34b8087b8c29bb46a02f5'
CLIENT_SECRET = '90e62985226f4e718232b3314f4ab8b2'
credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
SPOTIFY = spotipy.Spotify(client_credentials_manager=credentials_manager)

REM = 16

df = pd.read_csv('music_genre.csv')


#Song
class Song:
    def __init__(self,instance_id,artist_name,track_name,popularity,acousticness,
                 danceability,duration_ms, energy,instrumentalness,key,liveness,
                 loudness,mode,speechiness,tempo,obtained_date,valence,music_genre) -> None:
        
        self.__song_id = instance_id
        self.__artist_name = artist_name
        self.__name = track_name
        self.__popularity = popularity
        self.__duration_ms = duration_ms
        self.__danceability = danceability
        self.__energy = energy
        self.__key = key
        self.__mode = mode
        self.__speechiness = speechiness
        self.__acousticness = acousticness
        self.__instrumentalness = instrumentalness
        self.__liveness = liveness
        self.__loudness = loudness
        self.__date = obtained_date
        self.__valance = valence
        self.__tempo = tempo
        self.__genre = music_genre
    
    def get_id(self):
        return self.__song_id

    def get_name(self):
        return self.__name
    
    def get_danceability(self):
        return self.__danceability
    
    def get_energy(self):
        return self.__energy
    
    def get_acousticness(self):
        return self.__acousticness
    
    def get_instrumentalness(self):
        return self.__instrumentalness
    
    def get_tempo(self):
        return self.__tempo

def create_song_from_row(row):
    return Song(
        row['instance_id'],
        row['artist_name'],
        row['track_name'],
        row['popularity'],
        row['acousticness'],
        row['danceability'],
        row['duration_ms'],
        row['energy'],
        row['instrumentalness'],
        row['key'],
        row['liveness'],
        row['loudness'],
        row['mode'],
        row['speechiness'],
        row['tempo'],
        row['obtained_date'],
        row['valence'],
        row['music_genre'],
        )

class NearestNeighbors:
    def __init__(self, n_neighbors) -> None:
        self.n_neighbors = n_neighbors
        self.songs = {}
    
   
    def fit(self,songs):
        self.songs = {song.get_id(): song for song in songs}
    
    def kneighbors(self,song):
        distances = []
        for song_id,s in self.songs.items():
            distance = euclidean_distance(song,s)
            distances.append((distance, s))
        
        distances.sort(key=lambda x:x[0])
        
        neighbors = [neighbor for _ , neighbor in distances[1:self.n_neighbors+1]]
        
        return neighbors
 
def euclidean_distance(song1, song2):
    attributes1 = [song1.get_danceability(), song1.get_energy(), song1.get_acousticness(), song1.get_instrumentalness()]
    attributes2 = [song2.get_danceability(), song2.get_energy(), song2.get_acousticness(), song2.get_instrumentalness()]
    squared_diff = [(a - b) ** 2 for a, b in zip(attributes1, attributes2)]
    return math.sqrt(sum(squared_diff))





class DirIconPath:
    def __init__(self) -> None:
        self.__abs_program_path = os.path.abspath(__file__)
        self.__abs_dir_program = os.path.dirname(self.__abs_program_path)
        self.__dir_icon_path = os.path.join(self.__abs_dir_program,'img')
    
    def getIconFilePath(self,name_icon_file):
        file_path = os.path.join(self.__dir_icon_path,name_icon_file)
        return file_path


class MainPalletColor:
    BLACK = '#222831'
    PRINCIPAL = '#DDDDDD'
    CONTRAST = '#F05454'
    LIGHT = '#EEEEEE'
    SHADOW = '#ababab'
    INTENSE_SHADOW = '#696969'


    
class ResizableItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self.hovered_index = None
        self.shadow_widget = None

    def paint(self, painter, option, index):
        if index == self.hovered_index:

            # Modificar el tamaño del rectángulo solo si el ítem está siendo resaltado
            option.rect.setHeight(60)  # Establecer la altura deseada aquí
            
        super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseMove:
            self.hovered_index = index
            self.parent().viewport().update()
        
        return super().editorEvent(event, model, option, index)
    
class CSVViewer(QTableView):
    def __init__(self,data,prev_csv_selecion_widget):
        super().__init__()
        self._data = data
        self._prev_csv_selection_widget = prev_csv_selecion_widget
        
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

        
        #self.entered.connect(self._print_index)
        
        delegate = ResizableItemDelegate(self)
        self.setItemDelegate(delegate)
        
        self.clicked.connect(self._print_index)
        
    def _print_index(self,index):
        selected_row = index.row()
        #track_name = str(self.model().data(self.model().index(selected_row, 0)))
        track_name = index.data()
        row_data = self._data[self._data['track_name'] == track_name].iloc[0]
        artist_name = row_data['artist_name']
        popularity = row_data['popularity']
        duration = row_data['duration_ms']
        obt = row_data['obtained_date']
        genre = row_data['music_genre']
        
        query = f'track:{track_name} artist:{artist_name}'
        result = SPOTIFY.search(q=query, type='track', limit=1)
        
        if result['tracks']['items']:
            album_cover_url = result['tracks']['items'][0]['album']['images'][1]['url']
            album_url = result['tracks']['items'][0]['album']['external_urls']['spotify']
            artist_url = result['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
            media_url = result['tracks']['items'][0]['preview_url']
        else:
            album_cover_url =''
            album_url = None
            artist_url = None
            media_url = None

            
        print(album_cover_url)
        
        self._prev_csv_selection_widget.update_data(track_name, artist_name, popularity, duration, obt, genre,album_cover_url,album_url,artist_url,media_url)
      
    
class PrevCsvSelection(QWidget):
    def __init__(self):
        super().__init__()
        #Dir Icon Path
        dir_icon_path = DirIconPath()
        #Layouts
        main_layout = QVBoxLayout()
        info_song_layout = QFormLayout()
        buttons_layout = QHBoxLayout()
        
        
        self.__album_image = QLabel()
        self.__album_image.setObjectName('album-cover-img')
        main_layout.addWidget(self.__album_image,alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(info_song_layout)
        
        info_song_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        info_song_layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #Buttons
        self.__artist_button = IconButton(
            dir_icon_path.getIconFilePath('artista-white-icon.png'),
            dir_icon_path.getIconFilePath('artista-black-icon.png'),
            True)
        
        self.__album_button = IconButton(
            dir_icon_path.getIconFilePath('album-white-icon.png'),
            dir_icon_path.getIconFilePath('album-black-icon.png'),
            True
        )
        self.__preview_play_button = PlayMediaIconButton(
            dir_icon_path.getIconFilePath('play-white-icon.png'),
            dir_icon_path.getIconFilePath('play-black-icon.png'),
            True
        )
            
        
        self._artist_url = None
        self._album_url = None
        self.__artist_button.clicked.connect(self._open_artist_spotify)
        self.__album_button.clicked.connect(self._open_album_spotify)
        
        buttons_layout.addWidget(self.__artist_button,alignment=Qt.AlignmentFlag.AlignHCenter)
        buttons_layout.addWidget(self.__album_button,alignment=Qt.AlignmentFlag.AlignHCenter)
        buttons_layout.addWidget(self.__preview_play_button,alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.addLayout(buttons_layout)
        
        self.__track_name_label = QLabel()
        self.__artist_name_label = QLabel()
        self.__popularity_label = QLabel()
        self.__duration_label = QLabel()
        self.__obt_label = QLabel()
        self.__genre = QLabel()
        
        info_song_layout.addRow('Nombre: ',self.__track_name_label)
        info_song_layout.addRow('Artista: ',self.__artist_name_label)
        info_song_layout.addRow('Popularidad: ',self.__popularity_label)
        info_song_layout.addRow('Duration: ',self.__duration_label)
        info_song_layout.addRow('Fecha de Lanzamiento: ',self.__obt_label)
        info_song_layout.addRow('Genero: ',self.__genre)
        
        
        self.setObjectName('csv-selection')
        self.setLayout(main_layout)
        # Crear el efecto de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(MainPalletColor.SHADOW))
        shadow.setOffset(0, 0)

        # Aplicar el efecto de sombra al widget
        self.setGraphicsEffect(shadow)
        self.setMaximumSize(325,500)
        self.setMinimumSize(325,500)
    
    def update_data(self, track_name, artist_name, popularity, duration, obt, genre,album_cover_url,album_url,artist_url,media_url):
        self.__track_name_label.setText(track_name)
        self.__artist_name_label.setText(artist_name)
        self.__popularity_label.setText(str(popularity))
        self.__duration_label.setText(str(duration))
        self.__obt_label.setText(obt)
        self.__genre.setText(genre)
        
        if media_url != None:
            self.__preview_play_button.set_media_url(media_url)
        
        if album_url != None:
            self._album_url = album_url
        else:
            self._album_url = None
        
        if artist_url != None:
            self._artist_url = artist_url
        else:
            self._artist_url = None
        
        if album_cover_url:
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(album_cover_url).content)
            self.__album_image.setPixmap(pixmap.scaled(300,300))
            
        else:
            self.__album_image.clear()
        
    
    def _open_album_spotify(self):
        if self._album_url != None:
            QDesktopServices.openUrl(QUrl(self._album_url))
        
    def _open_artist_spotify(self):
        if self._artist_url != None:
            QDesktopServices.openUrl(QUrl(self._artist_url))
        
    
    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget,o,painter,self)
        
        
class IconButton(QPushButton):
    def __init__(self,icon_path,togle_icon_path='',toogle=False,text='',objectName=None):
        super().__init__(text=text)
        self._toogle_icon_path = ''
        self._toogle_icon = None
        self._main_icon = QIcon(icon_path)

        if objectName != None:
            self.setObjectName(objectName)
        if toogle != False:
            self._toogle_icon_path = togle_icon_path
            self._toogle_icon = QIcon(self._toogle_icon_path)
        
          
        self.setIcon(QIcon(self._main_icon))
        self.setMinimumSize(40,40)
        self.setMaximumSize(40,40)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(MainPalletColor.SHADOW))
        shadow.setOffset(0,0)
        self.setGraphicsEffect(shadow)
        
    def enterEvent(self, event) -> None:
        if self._toogle_icon_path != '':
            self.setIcon(self._toogle_icon)
        super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        self.setIcon(self._main_icon)
        super().leaveEvent(event)

class PlayMediaIconButton(IconButton):
    def __init__(self, icon_path,togle_icon_path='', toogle=False,media_url=None, text='', objectName=None):
        super().__init__(icon_path, togle_icon_path, toogle, text, objectName)
        self.setCheckable(True)
        abs_program_path = os.path.abspath(__file__)
        program_dir_path = os.path.dirname(abs_program_path)
        self._media_url = media_url
        self._media_file_name = 'preview.mp3'
        self._media_path = os.path.join(program_dir_path,self._media_file_name)
        self._media_player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._media_player.setAudioOutput(self._audio_output)
        
        self.clicked.connect(self.play_media)
     
    def play_media(self,checked):
        self._media_player.setPosition(0)
        self._media_player.setSource(QUrl(self._media_file_name))
        self._media_player.play()
        
    def set_media_url(self,value):
        self._media_url = value
        response = requests.get(self._media_url)
        with open(self._media_file_name, "wb") as file:
            file.write(response.content)
            
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
        self.__seeker.setObjectName('seeker-input')
        shadow_seeker = QGraphicsDropShadowEffect()
        shadow_seeker.setBlurRadius(10)
        shadow_seeker.setColor(QColor(MainPalletColor.SHADOW))
        shadow_seeker.setOffset(0,0)
        self.__seeker.setGraphicsEffect(shadow_seeker)

        self.__find_button = CustomButton('Search','search-button')
        
        
        self.__prev_csv_selection = PrevCsvSelection()

        csv_viewer = CSVViewer(df,self.__prev_csv_selection)
        
        #WidgetWindow Right
        self.__right_window_widget = QWidget()
        right_layout = QVBoxLayout()
        
        #Generate List Button
        self.__generate_list_button = CustomButton('Generate List','generate-list-button')
        
        
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

        search_section_layout.addWidget(self.__seeker,alignment=Qt.AlignmentFlag.AlignVCenter)
        search_section_layout.addWidget(self.__find_button,alignment=Qt.AlignmentFlag.AlignVCenter)
        left_layout.addWidget(csv_viewer)
        
        
       
        
        background = QWidget()
        background.setLayout(principal_layout)
        background.setObjectName('background')
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
