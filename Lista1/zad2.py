import networkx as nx
from pathlib import Path
from random import uniform, randint

file = Path("graf_euler.edgelist")
if file.is_file():
    file = open("graf_euler.edgelist", "rb")
    G = nx.read_edgelist(file, create_using=nx.MultiGraph, nodetype=int)
    file.close()

    se, e = nx.is_semieulerian(G), nx.is_eulerian(G)
    if e: print("Graf posiada ścieżkę i cykl eulerowski")
    elif se: print("Graf posiada tylko ścieżkę eulerowską")
    else: print("Graf nie posiada ani ścieżki ani cyklu eulerowskiego")

else:
    while True:
        G = nx.fast_gnp_random_graph(randint(100, 150), uniform(0.05, 0.25))
        if nx.is_eulerian(G) or nx.is_semieulerian(G):
            file = open("graf_euler.edgelist", "wb")
            nx.write_edgelist(G, file)
            file.close()
            break

