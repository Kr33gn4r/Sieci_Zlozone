import pandas as pd
import networkx as nx
import matplotlib
import copy
import random
from matplotlib import pyplot as plt

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
    print(f"Współczynnik gronowania = {nx.average_clustering(graph)}")

def random_node_deletion(graph: nx.Graph, amount, step):
    G = copy.deepcopy(graph)
    node_amount_to_delete = 1

    diam, sp, clust = [nx.diameter(G)], [nx.average_shortest_path_length(G)], [nx.average_clustering(G)]

    for _ in range(amount):
        nodes = list(G.nodes())
        nodes_to_delete = random.sample(nodes, node_amount_to_delete)
        G.remove_nodes_from(nodes_to_delete)

        try:
            diam.append(nx.diameter(G))
        except Exception:
            diam.append(float("inf"))

        try:
            sp.append(nx.average_shortest_path_length(G))
        except Exception:
            sp.append(float("inf"))

        try:
            clust.append(nx.average_clustering(G))
        except Exception:
            clust.append(float("inf"))

        print(f"{diam=}\n{sp=}\n{clust=}")

    return diam, sp, clust

def dedicated_node_deletion(graph: nx.Graph, amount, step):
    G = copy.deepcopy(graph)
    node_amount_to_delete = 1

    diam, sp, clust = [nx.diameter(G)], [nx.average_shortest_path_length(G)], [nx.average_clustering(G)]

    for _ in range(amount):
        degrees = dict(G.degree())
        nodes_to_delete = sorted(degrees, key=degrees.get, reverse=True)[:node_amount_to_delete]
        G.remove_nodes_from(nodes_to_delete)

        try:
            diam.append(nx.diameter(G))
        except Exception:
            diam.append(float("inf"))

        try:
            sp.append(nx.average_shortest_path_length(G))
        except Exception:
            sp.append(float("inf"))

        try:
            clust.append(nx.average_clustering(G))
        except Exception:
            clust.append(float("inf"))

        print(f"{diam=}\n{sp=}\n{clust=}")

    return diam, sp, clust

def pagerank_plot(pagerank):
    sorted_values = sorted(pagerank.values(), reverse=True)

    x_vals = range(1, len(sorted_values) + 1)
    y_vals = sorted_values

    plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='b')
    plt.xlabel('Wierzchołki (posortowane według PageRank)')
    plt.ylabel('PageRank')
    plt.title('PageRank dla wierzchołków')
    plt.show()

def plot_removals(diam, sp, clust):
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    axs[0].plot(range(0, len(diam)), diam, label='Zmiany średnicy', color='b')
    axs[0].set_title('Zmiany średnicy')

    # Wykres 2: Zmiany średniej najkrótszej ścieżki
    axs[1].plot(range(0, len(sp)), sp, label='Zmiany średniej najkrótszej ścieżki', color='g')
    axs[1].set_title('Zmiany średniej najkrótszej ścieżki')

    # Wykres 3: Zmiany współczynnika gronowania
    axs[2].plot(range(0, len(clust)), clust, label='Zmiany współczynnika gronowania', color='r')
    axs[2].set_title('Zmiany współczynnika gronowania')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    CONST_ADDR = 'datasets/'
    df = pd.read_csv(CONST_ADDR + 'government_edges.csv')
    oG = nx.Graph()
    oG.add_edges_from(df[['node_1', 'node_2']].values)

    #parameters_of_graph(G)

    #random_node_deletion(oG, 10, 0.005)
    #dedicated_node_deletion(oG, 10, 0.005)

    #pagerank = nx.pagerank(oG)
    #pagerank_plot(pagerank)

    diam = [10, 10, 10, 10, 10, 10, 10]
    sp = [3.7805595881543774, 3.7807916339226453, 3.7807285580889913, 3.780643667165663, 3.7808432378213498,
          3.780643812397512, 3.780712945765124]
    clust = [0.41088422622445286, 0.4108081614160076, 0.41081894089274007, 0.41083687746219905, 0.41093452216518267,
             0.41090478973095457, 0.410892761614953, 0.4108815231982924, 0.4109428453767357, 0.41092338217400115,
             0.41084700752156494]
    plot_removals(diam, sp, clust)

    diam = [10, 10, 10]
    sp = [3.7805595881543774, 3.782304608590424, 3.810723472284374]
    clust = [0.41088422622445286, 0.41043207155082356, 0.40973281227268016, 0.4062060448616858, 0.4048562607862032,
             0.40417298447368644, 0.4036710240013021, 0.4022787731371087, 0.40173901185898114, 0.4012165643678442,
             0.40056662660970893]
    plot_removals(diam, sp, clust)