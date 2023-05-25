from abc import ABC,abstractclassmethod
from itertools import combinations
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math

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

class SongCreator(ABC):
    @abstractclassmethod
    def from_dict(self,row):
        return Song(
        row['id'],
        row['name'],
        row['popularity'],
        row['duration_ms'],
        row['explicit'],
        row['artists'],
        row['id_artists'],
        row['release_date'],
        row['danceability'],
        row['energy'],
        row['key'],
        row['mode'],
        row['speechiness'],
        row['acousticness'],
        row['instrumentalness'],
        row['liveness'],
        row['valence'],
        row['tempo'],
        row['time_signature']
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

def euclidean_distance(song1, song2):
    attributes1 = [song1.get_danceability(), song1.get_energy(), song1.get_acousticness(), song1.get_instrumentalness()]
    attributes2 = [song2.get_danceability(), song2.get_energy(), song2.get_acousticness(), song2.get_instrumentalness()]
    squared_diff = [(a - b) ** 2 for a, b in zip(attributes1, attributes2)]
    return math.sqrt(sum(squared_diff))


  
df = pd.read_csv('music_genre.csv')
graph = nx.Graph()
songs = df.apply(create_song_from_row,axis=1).tolist()

graph.add_nodes_from(songs)


#Vecinos cercanos
n_neighbors = 10
nn = NearestNeighbors(n_neighbors)
nn.fit(songs)
contador =0        
distances = {}

for song in songs:
    neighbors = nn.kneighbors(song)
    for neighbor in neighbors:
        neighbor_id = neighbor.get_id()
        
        if neighbor_id not in distances:
            distance_value = euclidean_distance(song,neighbor)
            distances[neighbor_id] = distance_value
        
        else:
            distance_value = distances[neighbor_id]
                
        graph.add_edge(song,neighbor,weight=distance_value)
        print('Agrega Arista',len(graph.edges))

 
# Mostrar pesos de las aristas y nodos conectados
for u, v, weight in graph.edges.data('weight'):
    print("Nodo 1:", u.get_name())
    print("Nodo 2:", v.get_name())
    print("Peso de la arista:", weight)
    print("---")




"""
def euclidean_distance(song1, song2):
    attributes1 = [song1.danceability, song1.energy, song1.acousticness, song1.instrumentalness, song1.tempo]
    attributes2 = [song2.danceability, song2.energy, song2.acousticness, song2.instrumentalness, song2.tempo]
    squared_diff = [(a - b) ** 2 for a, b in zip(attributes1, attributes2)]
    return math.sqrt(sum(squared_diff))

# Crear un grafo no dirigido
graph = nx.Graph()

# Agregar los nodos al grafo
for song in songs:  
    graph.add_node(song)

# Calcular el peso de las aristas utilizando distancia euclidiana
for i in range(len(songs)):
    for j in range(i+1, len(songs)):
        song1 = songs[i]
        song2 = songs[j]
        distance_value = euclidean_distance(song1, song2)
        graph.add_edge(song1, song2, weight=distance_value)
        

print('Nodos del grafo')
for node in graph.nodes():
    print(node.get_name())
"""
        
        

