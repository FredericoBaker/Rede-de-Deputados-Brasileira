import networkx as nx
import pandas as pd
from itertools import combinations
import pickle

# Classe com as funções necessárias para a criação e manipulação dos grafos
class Votos():

    def __init__(self):
        deputados_data = pd.read_csv(f'./dados-limpos/deputados.csv')
        votos_data = pd.read_csv(f'./dados-limpos/votos.csv')

    # Cria um grafo para um ano específico
    def graph_by_year(self, year):
        self.votos_data['dataHoraVoto'] = pd.to_datetime(self.votos_data['dataHoraVoto']) 
        
        votos_data_year = self.votos_data[self.votos_data['dataHoraVoto'].dt.year == year]

        G = nx.Graph()

        for id_votacao, group in votos_data_year.groupby('idVotacao'):

            for voto, voto_group in group.groupby('voto'):

                for dep1, dep2 in combinations(voto_group['deputado_id'], 2):
                    
                    if G.has_edge(dep1, dep2):
                        G[dep1][dep2]['weight'] += 1
                    else:
                        G.add_edge(dep1, dep2, weight=1)

        return G
    
    # Cria um grafo para um "term" ou legislatura
    def graph_by_term(self, term):
        votos_data_term = self.votos_data[self.votos_data['deputado_idLegislatura'] == term]
        
        G = nx.Graph()

        for id_votacao, group in votos_data_term.groupby('idVotacao'):

            for voto, voto_group in group.groupby('voto'):

                for dep1, dep2 in combinations(voto_group['deputado_id'], 2):
                    
                    if G.has_edge(dep1, dep2):
                        G[dep1][dep2]['weight'] += 1
                    else:
                        G.add_edge(dep1, dep2, weight=1)

        return G

    # Salva o grafo em path
    def save_graph(self, G, path):

        with open(path, 'wb') as file:
            pickle.dump(G, file)

            print(f'Graph saved in {path}.')
            return True
        
    # Acessa um grafo salvo
    def get_graph(self, path):

        with open(path, 'rb') as file:
            return pickle.load(file)