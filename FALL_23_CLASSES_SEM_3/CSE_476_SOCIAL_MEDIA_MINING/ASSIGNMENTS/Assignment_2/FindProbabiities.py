import networkx as nx
def calculate_probabilities(G):
  """Calculates the probability that a new node follows other nodes and the probability that a new node is followed by others in a followee/follower network using the preferential attachment model.

  Args:
    G: A NetworkX graph object representing the followee/follower network.

  Returns:
    A tuple containing the probability that a new node follows other nodes and the probability that a new node is followed by others.
  """

  # Calculate the in-degree and out-degree of each node.
  in_degrees = nx.in_degree_centrality(G)
  out_degrees = nx.out_degree_centrality(G)

  # Calculate the probability that a new node follows a particular node.
  p_follow = {}
  for node in G.nodes():
    p_follow[node] = in_degrees[node] / sum(in_degrees.values())

  # Calculate the probability that a new node is followed by a particular node.
  p_followed = {}
  for node in G.nodes():
    p_followed[node] = out_degrees[node] / sum(out_degrees.values())

  return p_follow, p_followed


def update_values(G, a, b):
  """Updates the values in the preferential attachment algorithm.

  Args:
    G: A NetworkX graph object representing the followee/follower network.
    a: The number of edges that each new node will follow.
    b: The number of edges that each new node will be followed by.
  """

  # Calculate the in-degree and out-degree of each node.
  in_degrees = nx.in_degree_centrality(G)
  out_degrees = nx.out_degree_centrality(G)

  # Calculate the probability that a new node will follow a node.
  p_follow = {}
  for node in G.nodes():
    p_follow[node] = in_degrees[node] / sum(in_degrees.values())

  # Calculate the probability that a new node will be followed by a node.
  p_followed = {}
  for node in G.nodes():
    p_followed[node] = out_degrees[node] / sum(out_degrees.values())

  # Update the values in the graph.
  for node in G.nodes():
    d_out = G.out_degree(node)
    d_in = G.in_degree(node)

    # Follow a nodes with probability proportional to their in-degree.
    while d_out < a:
      node_to_follow = nx.weighted_choice(list(G.nodes()), p_follow.values())
      G.add_edge(node, node_to_follow)
      d_out += 1

    # Be followed by b nodes with probability proportional to their out-degree.
    while d_in < b:
      node_to_be_followed_by = nx.weighted_choice(list(G.nodes()), p_followed.values())
      G.add_edge(node_to_be_followed_by, node)
      d_in += 1


# Example usage:

G = nx.DiGraph()
G.add_edge(1, 2)
G.add_edge(1, 4)
G.add_edge(1, 5)
G.add_edge(2, 3)
G.add_edge(2, 5)
G.add_edge(2, 4)
G.add_edge(4, 5)
G.add_edge(5, 6)
G.add_edge(5, 3)
G.add_edge(5, 2)
G.add_edge(6, 3)

# Calculate the probabilities.
p_follow, p_followed = calculate_probabilities(G)
# Print the probabilities.
print(p_follow)
print(p_followed)
# Add a new node with a = 4 and b = 3.
update_values(G, 4, 3)
# Calculate the probabilities.
p_follow, p_followed = calculate_probabilities(G)
# Print the probabilities.
print(p_follow)
print(p_followed)
# Add a new node with a = 4 and b = 3.
update_values(G, 2, 4)
# Calculate the probabilities.
p_follow, p_followed = calculate_probabilities(G)

# Print the probabilities.
print(p_follow)
print(p_followed)



