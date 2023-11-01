import networkx as nx
from typing import List, Tuple

def parameters_of_graph(graph: nx.Graph):
    if isinstance(graph, nx.Graph):
        print(f"Jest to graf prosty, nieskierowany,", sep=" ")
    elif isinstance(graph, nx.DiGraph):
        print(f"Jest to graf prosty, skierowany,", sep=" ")
    elif isinstance(graph, nx.MultiGraph):
        print(f"Jest to multigraf, nieskierowany,", sep=" ")
    else:
        print(f"Jest to multigraf, skierowany,", sep=" ")

    if nx.is_weighted(graph):
        print(f"ważony,", sep=" ")
    else:
        print(f"nieważony,", sep=" ")

    if nx.is_connected(graph):
        print(f"spójny,", sep=" ")
    else:
        print(f"niespójny,", sep=" ")

    if nx.is_planar(graph):
        print(f"planarny,", sep=" ")
    else:
        print(f"nieplanarny,", sep=" ")




    print(f"Rząd = {graph.number_of_nodes()}")
    print(f"Rozmiar = {graph.number_of_edges()}")

    """
    dwudzielny, pełny, przypadkowy
    rząd, rozmar, gęstość, średnica, średnia długośc ścieżki
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


