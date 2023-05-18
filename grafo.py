import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

df = pd.read_csv('tracks.csv')
G = nx.Graph()

selected_features = ['danceability', 'energy', 'tempo', 'acousticness']
corr_matrix = np.corrcoef(df[selected_features].T)

# Agregar cada canción como un nodo al grafo
for i, row in df.iterrows():
    G.add_node(row['name'], id=row['id'], popularity=row['popularity'], duration=row['duration_ms'], explicit=row['explicit'], artists=row['artists'], id_artists=row['id_artists'], release_date=row['release_date'], danceability=row['danceability'],energy=row['energy'], key=row['key'], loudness=row['loudness'], mode=row['mode'], speechiness=row['speechiness'], acousticness=row['acousticness'], instrumentalness=row['instrumentalness'], liveness=row['liveness'], valence=row['valence'], tempo=row['tempo'], time_signature=row['time_signature'])

# Agregar las aristas al grafo
for i in range(len(selected_features)):
    for j in range(i+1, len(selected_features)):
        similarity = corr_matrix[i, j]
        print(similarity)
        if similarity > 0.5:
            for k, row_k in df.iterrows():
                for l, row_l in df.iterrows():
                    if k != l and row_k['name'] == row_l['name']:
                        G.add_edge(row_k['name'], row_l['name'], weight=similarity)



print(G.number_of_edges())


