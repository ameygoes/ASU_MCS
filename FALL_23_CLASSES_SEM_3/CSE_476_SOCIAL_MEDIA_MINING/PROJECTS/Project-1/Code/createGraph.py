import networkx as nx
import matplotlib.pyplot as plt

def get_followers(mastodon, user_id):
    followers = mastodon.account_followers(user_id)
    follower_ids = {follower.id for follower in followers}
    return follower_ids

def get_followees(mastodon, user_id):
    followees = mastodon.account_following(user_id)
    followee_ids = {followee.id for followee in followees}
    return followee_ids


def create_friendship_network(G, data_list, mastodon):
    user_ids = set(user['account_id'] for user in data_list)

    for user_id in user_ids:
        G.add_node(user_id, label=user_id)  # Add a node for each user

    for user in data_list:
        user_id = user['account_id']
        followers = get_followers(mastodon, user_id)
        followees = get_followees(mastodon, user_id)

        if followers and followees:
            for follower_id in followers:
                if (follower_id in user_ids) and (not G.has_edge(follower_id, user_id)):
                    G.add_edge(user_id, follower_id)  # Add an edge for each follower

            for followee_id in followees:
                if (followee_id in user_ids) and (not G.has_edge(follower_id, user_id)):
                    G.add_edge(user_id, followee_id)  # Add an edge for each followee

    return G

def create_graph(G, followers, followees):
    # Add nodes for followers and followees
    for user in followers:
        G.add_node(user["id"], label=user["username"], type="follower")

    for user in followees:
        G.add_node(user["id"], label=user["username"], type="followee")

    # Add edges to represent relationships (follows)
    for user in followers:
        for followee in followees:
            G.add_edge(user["id"], followee["id"])
    

def visualize_graph(G):
    pos = nx.spring_layout(G, seed=42) 
    labels = nx.get_node_attributes(G, "label")
    nx.draw(G, pos, with_labels=True, node_size=10,  labels=labels, node_color="skyblue", font_size=6)
    plt.title("Friendship Network")
    plt.show()
