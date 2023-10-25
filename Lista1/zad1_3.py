import networkx as nx

file = open("higgs.edgelist", "rb")
G = nx.read_edgelist(file, nodetype=int, data=(("weight", int),))
file.close()

# ------------------------------------------------------------------------------------
start_point: int = 29903    # także jest źródłem w przepływach
end_point: int = 432962     # także jest ujściem w przepływach
# ------------------------------------------------------------------------------------

try:
    print(f"Najkrótszą ścieżką z {start_point = } do {end_point = } jest \n"
          f"{nx.dijkstra_path(G, start_point, end_point)} \n"
          f"o długości {nx.dijkstra_path_length(G, start_point, end_point)}")
except nx.NodeNotFound:
    print(f"{start_point = } nie znajduje się w grafie")
except nx.NetworkXNoPath:
    print(f"Nie istnieje żadna ścieżka pomiędzy {start_point = } i {end_point = }")
print()

try:
    test: nx.DiGraph = nx.algorithms.flow.edmonds_karp(G, start_point, end_point, capacity="weight")
    print(f"Maksymalny przepływ w grafie rezydualnym z {start_point = } do {end_point = } wynosi "
          f"{test.graph['flow_value']}")
except nx.NetworkXUnbounded:
    print(f"Graf posiada ścieżke o nieskończonej pojemności / wadze")


