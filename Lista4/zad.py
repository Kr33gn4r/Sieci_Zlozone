import networkx as nx
import matplotlib
import pandas as pd
import community
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from typing import List, Tuple, Dict
from collections import defaultdict
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.sparse.linalg import eigsh
from networkx.algorithms.community import modularity
matplotlib.use('TkAgg')


def cliques(graph: nx.Graph) -> None:
    all_cliques = sorted(list(nx.find_cliques(graph)), key=len, reverse=True)
    pos = nx.kamada_kawai_layout(graph)
    nx.draw(graph, pos, with_labels=True)

    colors = cm.get_cmap('rainbow', len(all_cliques))
    data = {"rozmiar": [], "klika": []}
    for i, clique in enumerate(all_cliques):
        nx.draw_networkx_nodes(graph, pos, nodelist=clique, node_color=colors(i), node_size=200)
        data["rozmiar"].append(len(clique))
        data["klika"].append(clique)

    df = pd.DataFrame(data)
    print(df)
    plt.show()


def modules(graph: nx.Graph) -> None:
    partition = community.best_partition(graph)
    communities = defaultdict(list)
    for node, id in partition.items():
        communities[id].append(node)
    pos = nx.kamada_kawai_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    colors = cm.get_cmap('rainbow', len(communities.keys()))

    data = {"rozmiar": [], "moduł": []}
    for i, x in enumerate(sorted(communities.values(), key=len, reverse=True)):
        nx.draw_networkx_nodes(graph, pos, nodelist=x, node_color=colors(i), node_size=200)
        data["rozmiar"].append(len(x))
        data["moduł"].append(x)

    df = pd.DataFrame(data)
    print(df)
    plt.show()


def agglomerate(graph: nx.Graph, threshold=6) -> Dict:
    adj_matrix = nx.to_numpy_array(graph)
    agglomerative_clusters = linkage(adj_matrix, method='ward')
    agglomerative_labels = fcluster(agglomerative_clusters, t=threshold, criterion='distance')

    for node, cluster in zip(graph.nodes, agglomerative_labels):
        graph.nodes[node]['agg'] = cluster

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    pos = nx.kamada_kawai_layout(graph)
    cmap = cm.get_cmap('rainbow', max(agglomerative_labels))

    nx.draw(graph, pos, node_color=[cmap(i) for i in agglomerative_labels], with_labels=False, ax=ax1)
    ax1.set_title("Analiza hierarchii skupień - metoda aglomeracyjna")

    agglomerative_dendrogram = dendrogram(agglomerative_clusters, color_threshold=threshold, ax=ax2, no_labels=True)
    ax2.set_title("Dendrogram - metoda aglomeracyjna")
    plt.show()

    modularity_agg = {}
    modularity_agg['ward'] = modularity(graph,
                                [{node for node, data in graph.nodes(data=True) if data['agg'] == cluster} for cluster
                                 in set(agglomerative_labels)])
    return modularity_agg


def divisive(graph: nx.Graph, threshold=3) -> Dict:
    adj_matrix = nx.to_numpy_array(graph)
    divisive_methods = ['single', 'complete', 'average', 'weighted', 'centroid']
    modularity_div = {}

    for method in divisive_methods:
        divisive_clusters = linkage(adj_matrix.T, method=method)
        divisive_labels = fcluster(divisive_clusters, t=threshold, criterion='distance')

        for node, cluster in zip(graph.nodes, divisive_labels):
            graph.nodes[node]['div'] = cluster

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        pos = nx.kamada_kawai_layout(graph)
        cmap = cm.get_cmap('rainbow', max(divisive_labels))

        nx.draw(graph, pos, node_color=[cmap(i) for i in divisive_labels], with_labels=False, ax=ax1)
        ax1.set_title(f"Analiza hierarchii skupień - metoda podziałowa {method}")

        divisive_dendrogram = dendrogram(divisive_clusters, ax=ax2, no_labels=True)
        ax2.set_title(f"Dendrogram - metoda podziałowa {method}")
        plt.show()

        modularity_div[method] = modularity(graph, [{node for node, data in graph.nodes(data=True) if data['div'] == cluster} for cluster in set(divisive_labels)])
    return modularity_div


def spectral(graph: nx.Graph, num_clusters=2, threshold=0.0) -> None:
    laplacian_matrix = nx.laplacian_matrix(graph)
    laplacian_array = laplacian_matrix.toarray().astype(float)
    eigenvalues, eigenvectors = eigsh(laplacian_array, k=num_clusters, which='SM') #smallest eigenvalues
    cutting_vector = eigenvectors[:, 1] #wybór kierunku podziału
    partition = [v >= threshold for v in cutting_vector]

    pos = nx.kamada_kawai_layout(graph)
    colors = ['red' if node_partition else 'blue' for node_partition in partition]
    nx.draw(graph, pos, node_color=colors, with_labels=False)
    plt.title("Partycjonowanie spektralne")
    plt.show()

if __name__ == "__main__":
    edges: List[Tuple] = []
    with open("bio-diseasome.mtx", 'r') as f:
        while tmp := f.readline().split(' '):
            if not tmp[0]: break
            tmp[0], tmp[1] = int(tmp[0]), int(tmp[1])
            edges.append((tmp[0], tmp[1]))
    graph: nx.Graph = nx.from_edgelist(edges)
    cliques(graph)
    modules(graph)
    md_agg = agglomerate(graph)
    md_div = divisive(graph)
    print(md_agg)
    print(md_div)
    spectral(graph)


"""
Klika w grafie to kompletny podgraf, w którym każda para wierzchołków jest połączona krawędzią. Oznacza to, że każdy 
    wierzchołek w klikce jest połączony z każdym innym wierzchołkiem.
Moduł w kontekście analizy sieci to grupa wierzchołków, które są silnie połączone wewnątrz grupy, a jednocześnie słabo 
    połączone z wierzchołkami spoza grupy. Moduły pomagają identyfikować struktury społeczne czy funkcjonalne w sieci.
Analiza hierarchii skupień (ang. hierarchical clustering) to technika grupowania, która tworzy hierarchię klastrów. 
    Węzły w dendrogramie reprezentują grupy, a odległość między nimi odzwierciedla podobieństwo między klastrami.
Dendrogram to drzewiasta struktura graficzna używana w analizie hierarchii skupień. Pokazuje, jak klastry są łączone 
    w miarę zbliżania się do korzenia drzewa.
Metoda aglomeracyjna to technika analizy hierarchii skupień, która zaczyna od pojedynczych obiektów i łączy je 
    stopniowo w większe klastry na podstawie określonego kryterium.
Metoda podziałowa to technika analizy hierarchii skupień, która zaczyna od jednego dużego klastra i dzieli go na 
    mniejsze klastry w miarę postępu.
    
Modularność to miara jakości podziału grafu na klastry. Wartości modularności oceniają, jak bardzo struktura klastrów 
    różni się od struktury losowej, a wyższe wartości wskazują na bardziej jednolity podział.
Metody aglomeracyjne:
- Są skuteczne w identyfikowaniu klastrów o nieregularnych kształtach.
- Dają hierarchiczne struktury klastrów, co może być korzystne, jeśli chcesz zobaczyć zarówno ogólną strukturę, jak i 
    bardziej szczegółowe podziały.
Metody podziałowe:
- Są bardziej skuteczne, gdy klastry są jednorodne, izolowane i wyraźnie odseparowane.
- Mogą działać lepiej, gdy klastry są bardziej równomierne w rozmiarze.

Podział spektralny to technika podziału grafu na podstawie analizy wartości i wektorów własnych jego macierzy Laplace'a.
    Proces ten wykorzystuje informacje związane z spektrum własnym grafu, czyli z jego własności spektralnych.
"""


