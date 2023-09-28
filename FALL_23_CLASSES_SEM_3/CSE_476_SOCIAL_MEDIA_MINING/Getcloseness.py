import networkx as nx

# Create an empty graph
G = nx.Graph()

# Add nodes and edges to your graph
G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2,6), (3,4), (3,5), (4,5), (4,6),(5,6)])

# Define alpha and beta
alpha = 0.25  # Adjust the value of alpha as needed
beta = 0.15   # Adjust the value of beta as needed

# Calculate Katz centrality with specified alpha and beta
katz_centrality = nx.katz_centrality(G, alpha=alpha, beta=beta)

# Print the Katz centrality values
print("Katz Centrality:")
print(katz_centrality)

betweenness_centrality = nx.betweenness_centrality(G)
print("Betweenness Centrality:")
print(betweenness_centrality)

closeness_centrality = nx.closeness_centrality(G)
print("Closeness Centrality:")
print(closeness_centrality)

# Choose a node for which you want to calculate the local clustering coefficient
node_of_interest = [1,3,5,6]

for node in node_of_interest:
# Calculate the local clustering coefficient for the chosen node
    local_clustering_coefficient = nx.clustering(G, node)

    print(f"Local Clustering Coefficient for Node {node}: {local_clustering_coefficient:.4f}")


# Nodes for which you want to calculate similarity
node_v3 = 3
node_v5 = 5

# Get the neighbors of node_v3 and node_v5
neighbors_v3 = set(G.neighbors(node_v3))
neighbors_v5 = set(G.neighbors(node_v5))

# Jaccard Similarity
jaccard_similarity = len(neighbors_v3.intersection(neighbors_v5)) / len(neighbors_v3.union(neighbors_v5))

# Cosine Similarity
cosine_similarity = len(neighbors_v3.intersection(neighbors_v5)) / (len(neighbors_v3) * len(neighbors_v5)) ** 0.5

print(f"Jaccard Similarity between v3 and v5: {jaccard_similarity:.4f}")
print(f"Cosine Similarity between v3 and v5: {cosine_similarity:.4f}")