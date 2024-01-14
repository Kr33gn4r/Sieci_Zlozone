from flask import Flask, jsonify
import networkx as nx
import random
import time
import pandas as pd

app = Flask(__name__)

# Wczytanie krawędzi z pliku CSV do G1
edges_df = pd.read_csv("government_edges.csv")
G1 = nx.from_pandas_edgelist(edges_df, "node_1", "node_2")

# Inicjalizacja pustego grafu G2
G2 = nx.Graph()

# Dodanie losowego podgrafu do G2
random_nodes = random.sample(list(G1.nodes()), 10)
G2.add_nodes_from(random_nodes)
G2.add_edges_from(G1.subgraph(random_nodes).edges())


def update_external_graph():
    # Metoda zewnętrzna - zwraca listę wierzchołków i krawędzi G2
    return jsonify(nodes=list(G2.nodes()), edges=list(G2.edges()))


def update_internal_graph():
    # Metoda wewnętrzna - co 60 sekund
    while True:
        time.sleep(5)

        # Wybierz losowy wierzchołek z G2
        random_node_G2 = random.choice(list(G2.nodes()))

        # Wybierz losowego sąsiada tego wierzchołka z G1
        neighbors_G1 = list(G1.neighbors(random_node_G2))
        if neighbors_G1:
            random_neighbor_G1 = random.choice(neighbors_G1)

            # Sprawdź, czy sąsiad jest już w G2
            if random_neighbor_G1 in G2:
                # Jeśli tak, usuń go z G2
                G2.remove_node(random_neighbor_G1)
            else:
                # Jeśli nie, dodaj go do G2 wraz z krawędziami
                G2.add_node(random_neighbor_G1)
                G2.add_edges_from(G1.subgraph(G2.nodes()).edges())


# Uruchomienie wątku dla metody wewnętrznej
import threading

threading.Thread(target=update_internal_graph, daemon=True).start()


@app.route('/get', methods=['GET'])
def get():
    return update_external_graph()


if __name__ == '__main__':
    app.run(debug=True)