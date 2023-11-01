import networkx as nx
from typing import List, Tuple

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


    """
    stopień wierzchołka, bliskość wierzchołka, pośrednictwo, stan (brak)
    pośrednictwo, waga, centralność wektora własnego, pagerank
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


