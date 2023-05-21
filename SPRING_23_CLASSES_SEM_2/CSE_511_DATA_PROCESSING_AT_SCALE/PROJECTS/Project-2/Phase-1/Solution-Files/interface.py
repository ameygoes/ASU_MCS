from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        query = '''
                    MATCH (a:Location{name: $start_node}), (d:Location{name: $last_node})
                    WITH id(a) AS source, [id(d)] AS targetNodes
                    CALL gds.bfs.stream($graphName, {sourceNode: source, targetNodes: targetNodes})
                    YIELD path RETURN path;
                '''
        
        with self._driver.session() as session:
            try:
                result = session.run(query, start_node=start_node, last_node=last_node, graphName='page_rank_graph')
                return result.data()
                
            except ServiceUnavailable:
                print("ERROR: Could not connect to the graph database.")
                return None

    def pagerank(self, max_iterations, weight_property):

        # CREATE GRAPH QUERY
        createGraph = "CALL gds.graph.project($graphName ,'Location','TRIP', {relationshipProperties: ['distance']});"

        with self._driver.session() as session:
            try:
                result = session.run(
                    createGraph,
                    graphName="page_rank_graph"
                )
            except:
                print("ERROR: Could not create graph.")
                return None


            try:
                result = session.run(
                    "CALL gds.pageRank.stream($graphName, { maxIterations: $maxIter, "
                    "relationshipWeightProperty: $weightProp}) "
                    "YIELD nodeId, score "
                    "RETURN gds.util.asNode(nodeId).name AS name, score "
                    "ORDER BY score DESC",
                    graphName="page_rank_graph",
                    maxIter=max_iterations,
                    weightProp=weight_property
                )
              
                nodes = []
                for record in result:
                    nodes.append(record.data())
                return [nodes[0], nodes[-1]]
                
            except ServiceUnavailable:
                print("ERROR: Could not connect to the graph database.")
                return None

