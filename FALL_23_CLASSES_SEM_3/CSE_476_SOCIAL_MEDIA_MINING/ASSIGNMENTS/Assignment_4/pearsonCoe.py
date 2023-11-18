import networkx as nx
import numpy as np

def calculate_pearson_coefficient(G, edges):
    # Get node attributes from the graph
    node_values = nx.get_node_attributes(G, 'ordinal_value')
    xl = []
    xr = []
    # Calculate the Pearson correlation coefficient for each edge
    for edge in edges:
        vi, vj = edge
        xl.append(node_values[vi])
        xr.append(node_values[vj])

        xl.append(node_values[vj])
        xr.append(node_values[vi])
    print(f"XL: {xl}")
    print(f"XR: {xr}")
    # Calculate the Pearson correlation coefficient
    r = np.corrcoef(xl, xr)[0, 1]

    return r

# Create a sample graph with ordinal values as node attributes and edges
G1 = nx.Graph()
G1.add_node(1, ordinal_value=19)
G1.add_node(2, ordinal_value=13)
G1.add_node(3, ordinal_value=21)
G1.add_node(4, ordinal_value=18)
G1.add_node(5, ordinal_value=22)
G1.add_node(6, ordinal_value=14)


G2 = nx.Graph()
G2.add_node(1, ordinal_value=19)
G2.add_node(2, ordinal_value=13)
G2.add_node(3, ordinal_value=21)
G2.add_node(4, ordinal_value=18)
G2.add_node(5, ordinal_value=22)
G2.add_node(6, ordinal_value=14)


# Define vi and vj for each edge
edges_1 = [(1, 2), (1, 5), (2, 3), (2, 4), (2, 5), (3, 5), (4, 5), (5, 6)]

edges_2 = [(1, 2), (1, 6), (2, 3), (2, 4), (3, 5), (4, 5), (4, 6), (5, 6)]

# Add edges to the graph
G1.add_edges_from(edges_1)
G2.add_edges_from(edges_2)


pc1 = calculate_pearson_coefficient(G1, edges_1)
print(f"Pearson coefficient: {pc1}")

pc2 = calculate_pearson_coefficient(G2, edges_2)
print(f"Pearson coefficient: {pc2}")

print(f"Homophily Index: {pc1 - pc2}")