from mastodon import Mastodon
from Mastodon_Toots import read_data_from_JSON
from configs import *
import networkx as nx

from createGraph import create_friendship_network, visualize_graph


mastodon = Mastodon(
    client_id = MASTODON_CLIENT_KEY,    
    client_secret = MASTODON_CLIENT_SECRET,    
    access_token = MASTODON_ACCESS_TOKEN ,  
    api_base_url = MASTODON_BASE_URL
)

controversial_hashtags = [
    'canada'
]
Finaltoots = []


# for hashtag in controversial_hashtags:
#     toots = []
#     limit = 1000
#     result = mastodon.timeline_hashtag(hashtag)
#     if len(result):
#         toots.extend(parse_toots(result))
#         page_next = None

#         while True:
#             page_next = mastodon.fetch_next(result)       
#             if page_next == result or not page_next:
#                 break
#             toots.extend(parse_toots(page_next))
#             result = page_next
            
#             if len(toots) >= limit:
#                 break
#     Finaltoots.extend(toots)
#     # resultSearchV2 = mastodon.search_v2(q=hashtag)
#     # print(json.dumps(resultSearchV2), indent = 4)
    

# store_to_json('toots.json', toots)
JSONList = read_data_from_JSON('toots.json')
# user_ids = get_user_ids(JSONList)

G = nx.Graph()
create_friendship_network(G, JSONList, mastodon)
visualize_graph(G)