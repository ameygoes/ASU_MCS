import networkx as nx

# Create a graph
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3),(1, 4), ( 1, 5), (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (4, 5), (5, 6)])

# Create a partition of the graph
partition = [{2, 4, 5}, {1, 6}, {3}]

# Create a subgraph view for each partition
subgraph_views = []
for community in partition:
    subgraph_views.append(G.subgraph(community))

# Calculate the modularity of each partition
modularity_partitions = []
for subgraph in subgraph_views:
    modularity_partitions.append(nx.algorithms.community.quality.modularity(subgraph, communities=partition))

# Subtract the modularity of the subgraph from the modularity of the entire graph
modularity_relative = []
modularity_global = nx.algorithms.community.quality.modularity(G, communities=partition)
for modularity_partition in modularity_partitions:
    modularity_relative.append(modularity_global - modularity_partition)

# Print the modularity of each partition
for modularity in modularity_relative:
    print(modularity)
