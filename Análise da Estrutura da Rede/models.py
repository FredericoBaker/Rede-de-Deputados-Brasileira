import networkx as nx
import pandas as pd
import numpy as np
from itertools import combinations
import pickle

# Classe com as funções necessárias para a criação e manipulação dos grafos
class Votos:
    def __init__(self, path):
        try:
            self.votos_data = pd.read_csv(path)
        except Exception as e:
            print(f"Error loading votos_data: {e}")
        

    # Cria um grafo para um ano específico
    def graph_by_year(self, year):
        self.votos_data['dataHoraVoto'] = pd.to_datetime(self.votos_data['dataHoraVoto'])
        votos_data_year = self.votos_data[self.votos_data['dataHoraVoto'].dt.year == year]

        G = nx.Graph()

        # Create a pivot table where each cell gives the vote of a particular deputy for a particular voting ID.
        pivot = votos_data_year.pivot(index='deputado_id', columns='idVotacao', values='voto')

        # For each pair of deputies, compute the similarity of their votes across all voting sessions.
        deputies = pivot.index.tolist()
        names = votos_data_year.set_index('deputado_id')['deputado_nome'].to_dict()  # Dictionary of deputies' names

        for dep_id, dep_name in names.items():
            G.add_node(dep_id, nome=dep_name)  # Add node with attribute of deputy's name

        for i, dep1 in enumerate(deputies):
            for j, dep2 in enumerate(deputies[i+1:], start=i+1):  # Start from i+1 to avoid self-comparison and double comparison
                
                # Vectorized computation of the similarity between two deputies
                votes_similarity = np.where(pivot.iloc[i] == pivot.iloc[j], 1, np.where((pivot.iloc[i].isna()) | (pivot.iloc[j].isna()), 0, -1)).sum()
                
                # Update the graph
                if G.has_edge(dep1, dep2):
                    G[dep1][dep2]['weight'] += votes_similarity
                else:
                    G.add_edge(dep1, dep2, weight=votes_similarity)

        return G
    
    # Cria um grafo para um "term" ou legislatura
    def graph_by_term(self, term):
        votos_data_term = self.votos_data[self.votos_data['deputado_idLegislatura'] == term]
        
        G = nx.Graph()

        # Create a pivot table where each cell gives the vote of a particular deputy for a particular voting ID.
        pivot = votos_data_term.pivot(index='deputado_id', columns='idVotacao', values='voto')

        # For each pair of deputies, compute the similarity of their votes across all voting sessions.
        deputies = pivot.index.tolist()
        names = votos_data_term.set_index('deputado_id')['deputado_nome'].to_dict()  # Dictionary of deputies' names

        for dep_id, dep_name in names.items():
            G.add_node(dep_id, nome=dep_name)  # Add node with attribute of deputy's name

        for i, dep1 in enumerate(deputies):
            for j, dep2 in enumerate(deputies[i+1:], start=i+1):  # Start from i+1 to avoid self-comparison and double comparison
                
                # Vectorized computation of the similarity between two deputies
                votes_similarity = np.where(pivot.iloc[i] == pivot.iloc[j], 1, np.where((pivot.iloc[i].isna()) | (pivot.iloc[j].isna()), 0, -1)).sum()
                
                # Update the graph
                if G.has_edge(dep1, dep2):
                    G[dep1][dep2]['weight'] += votes_similarity
                else:
                    G.add_edge(dep1, dep2, weight=votes_similarity)

        return G

    # Salva o grafo em path
    def save_graph(self, G, path):

        with open(path, 'wb') as file:
            pickle.dump(G, file)
            return
        
    # Acessa um grafo salvo
    def get_graph(self, path):

        with open(path, 'rb') as file:
            return pickle.load(file)