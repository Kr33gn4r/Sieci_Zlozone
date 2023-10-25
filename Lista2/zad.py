import networkx as nx
import pyvis
import numpy as np
import matplotlib
from typing import List, Tuple, Set
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')

def adjacency_matrix(edges: List[Tuple[int, int]], nodes: Set[int]) -> List[List[int]]:
    matrix: List[List[int]] = [[0 for _ in range(max(nodes) + 1)]
                               for _ in range(max(nodes) + 1)]
    for u, v in edges:
        matrix[u][v], matrix[v][u] = 1, 1
    return matrix

def incidence_matrix(edges: List[Tuple[int, int]], nodes: Set[int]) -> List[List[int]]:
    matrix: List[List[int]] = [[0 for _ in range(len(edges))]
                               for _ in range(max(nodes) + 1)]
    for idx, (u, v) in enumerate(edges):
        matrix[u][idx], matrix[v][idx] = 1, 1
    return matrix

def graph_from_adjacency(matrix: List[List[int]]) -> nx.Graph:
    matrix = np.array(matrix)
    rows, cols = np.where(matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

def graph_from_incidence(matrix: List[List[int]]) -> nx.Graph:
    edges: List = []
    matrix = np.array(matrix)
    for edge in matrix.T:
        edges.append(np.where(edge)[0])
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

if __name__ == "__main__":
    # noinspection PyTypeChecker
    edges: List[Tuple[int, int]] = []
    nodes: Set[int] = set()
    with open("bio-diseasome.mtx", 'r') as f:
        while tmp := f.readline().split(' '):
            if not tmp[0]: break
            tmp[0], tmp[1] = int(tmp[0]), int(tmp[1])
            nodes |= set(tmp)
            # noinspection PyTypeChecker
            edges.append((tmp[0], tmp[1]))

    adj_matrix = adjacency_matrix(edges, nodes)
    inc_matrix = incidence_matrix(edges, nodes)
    adjG = graph_from_adjacency(adj_matrix)
    incG = graph_from_incidence(inc_matrix)

    adjPos = nx.kamada_kawai_layout(adjG)
    incPos = nx.kamada_kawai_layout(incG)

    nx.draw(adjG, adjPos, node_size=100)
    plt.show()

    nx.draw(incG, incPos, node_size=100)
    plt.show()

    #nt = pyvis.network.Network()
    #nt.from_nx(adjG)
    #nt.show_buttons(filter_="physics")
    #nt.show('nx.html', notebook=False)