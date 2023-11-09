import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

matplotlib.use('TkAgg')

def parameters_of_graph(graph: nx.Graph) -> None:

    if isinstance(graph, nx.Graph):
        print(f"Jest to graf prosty, nieskierowany,", end=" ")
    elif isinstance(graph, nx.DiGraph):
        print(f"Jest to graf prosty, skierowany,", end=" ")
    elif isinstance(graph, nx.MultiGraph):
        print(f"Jest to multigraf, nieskierowany,", end=" ")
    else:
        print(f"Jest to multigraf, skierowany,", end=" ")

    if nx.is_weighted(graph):
        print(f"ważony,", end=" ")
    else:
        print(f"nieważony,", end=" ")

    if nx.is_connected(graph):
        print(f"spójny,", end=" ")
    else:
        print(f"niespójny,", end=" ")

    if nx.is_planar(graph):
        print(f"planarny,", end=" ")
    else:
        print(f"nieplanarny,", end=" ")

    if nx.is_bipartite(graph):
        print(f"dwudzielny.")
    else:
        print(f"niedwudzielny.")

    print()
    print(f"Rząd = {graph.number_of_nodes()},", end=" ")
    print(f"Rozmiar = {graph.number_of_edges()};", end=" ")
    if graph.number_of_edges() == \
            (graph.number_of_nodes() * (graph.number_of_nodes() - 1)) // 2:
        print(f"zatem jest to graf pełny.")
    else:
        print(f"zatem nie jest to graf pełny.")

    print(f"Gęstość = {nx.density(graph)}.")
    print(f"Średnica grafu = {nx.diameter(graph)},", end=" ")
    print(f"Średnia długość najkrótszej ścieżki = {nx.average_shortest_path_length(graph)}.")

    centralities = [
        {'function': nx.degree, 'title': 'Stopień wierzchołka'},
        {'function': nx.closeness_centrality, 'title': 'Bliskość wierzchołka'},
        {'function': nx.betweenness_centrality, 'title': 'Pośrednictwo krawędzi'},
        {'function': nx.eigenvector_centrality, 'title': 'Centralność eigenvectora'},
        {'function': nx.pagerank, 'title': 'Pagerank'},
    ]

    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    idx = 0
    for i in range(2):
        for j in range(3):
            if not (i == 1 and j == 1):
                current_centrality = centralities[idx]
                values = list(current_centrality['function'](graph).values()) if \
                    current_centrality['title'] != 'Stopień wierzchołka' else list(
                    dict(current_centrality['function'](graph)).values())
                median_value = np.median(values)
                mean_value = np.mean(values)

                n, bins, patches = axs[i, j].hist(values, bins=graph.number_of_nodes() // 10, edgecolor='black',
                                                  alpha=0.7)
                min_idx = np.digitize([min(bins)], bins)[0] - 1
                max_idx = np.digitize([max(bins)], bins)[0] - 1
                if min_idx < 0: min_idx = 0
                if max_idx > len(patches) - 1: max_idx = len(patches) - 1

                patches[min_idx].set_fc('blue')
                patches[max_idx].set_fc('orange')

                axs[i, j].axvline(median_value, color='red', linestyle='dashed', linewidth=2,
                                  label=f'Mediana: {median_value:.3f}')
                axs[i, j].axvline(mean_value, color='green', linestyle='dashed', linewidth=2,
                                  label=f'Średnia: {mean_value:.3f}')
                axs[i, j].axvline(min(bins), color='blue', linestyle='dashed', linewidth=2,
                                  label=f'Min: {min(bins):.3f}')
                axs[i, j].axvline(max(bins), color='orange', linestyle='dashed', linewidth=2,
                                  label=f'Max: {max(bins):.3f}')

                axs[i, j].legend()

                axs[i, j].set_xlabel(current_centrality['title'])
                if current_centrality['title'] == 'Pośrednictwo krawędzi':
                    ylabel = "Liczba krawędzi"
                else:
                    ylabel = "Liczba wierzchołków"
                axs[i, j].set_ylabel(ylabel)

                # Dodawanie tytułu dla wykresu
                axs[i, j].set_title(current_centrality["title"])
                idx += 1
            else:
                # Ukrywanie pustego subplotu
                axs[i, j].axis('off')

    plt.tight_layout()
    plt.show()

    """
    składowe spójne, k-spójność, przeguby i mosty
    klika n-tego rzędu, klika maksymalna, n-podklika
    graf połączeń (liczba połączeń/ile wierzchołków ją ma)
    czy bezskalowy
    """

if __name__ == "__main__":
    edges: List[Tuple] = []
    with open("bio-diseasome.mtx", 'r') as f:
        while tmp := f.readline().split(' '):
            if not tmp[0]: break
            tmp[0], tmp[1] = int(tmp[0]), int(tmp[1])
            edges.append((tmp[0], tmp[1]))
    graph: nx.Graph = nx.from_edgelist(edges)
    parameters_of_graph(graph)


