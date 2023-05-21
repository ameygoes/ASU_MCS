import time
import requests
import interface
from neo4j import GraphDatabase
import math
import sys

class TesterConnect:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def test_data_loaded(self):
        """
        Test to see if data is loaded into the database
            2. Run a query to get the number of nodes
            3. Run a query to get the number of edges
            4. Compare the results with the expected results
        """

        print("Testing if data is loaded into the database")

        with self._driver.session() as session:
            query = """
                MATCH (n)
                RETURN count(n) as num_nodes
            """
            result = session.run(query)
            num_nodes = result.data()[0]['num_nodes']

            query = """
                MATCH ()-[r]->()
                RETURN count(r) as num_edges
            """
            result = session.run(query)
            num_edges = result.data()[0]['num_edges']

            if (num_nodes == 90):
                print("\tCount of Edges is correct: PASS")
            else:
                print("\tCount of Edges is incorrect: FAIL")

            if (num_edges == 148):
                print("\tCount of Edges is correct: PASS")
            else:
                print("\tCount of Edges is incorrect: FAIL")

    def deleteGraph(self):
        with self._driver.session() as session:
            query = """
                CALL gds.graph.drop('page_rank_graph')
            """
            print("Deleting graph!")
            result = session.run(query)

    def deleteData(self):
        with self._driver.session() as session:
            query = """
                MATCH (n)-[r]-() DELETE r, n;
            """
            print("Deleting Nodes and Relations!")
            result = session.run(query)
def test_page_rank(max_iter, prop_name):
    """
    Test to see if PageRank implemented in interface is working
        1. Run a query to perform PageRank
        2. Compare the results with the expected results
    """


    conn = interface.Interface("neo4j://localhost:7687", "neo4j", "project2phase2")
    result = conn.pagerank(max_iter, prop_name)

    return result


def test_bfs(start_node, last_node):
    """
    Test to see if BFS implemeted in interface is working
        1. Run a query to perform a BFS
        2. Compare the results with the expected results
    """

    print("Testing if BFS is working")

    conn = interface.Interface("neo4j://localhost:7687", "neo4j", "project2phase2")
    result = conn.bfs(start_node, last_node)

    return result


def main():

    count = 0
    print("Trying to connect to server ", end="")
    sys.stdout.flush()
    while count < 10:
        try:
            response = requests.get("http://localhost:7474/")
            print("\nServer is running\n")
            break
        except:
            print(".", end="")
            sys.stdout.flush()
            count += 1
            time.sleep(5)

    print("----------------------------------")

    # Test load data
    tester = TesterConnect("neo4j://localhost:7687", "neo4j", "project2phase2")
    tester.test_data_loaded()
    tester.close()

    ansPageRank = {1: [[140, 0.6568516558905009], [88, 0.15000000000000002]],
           2: [[140, 0.7331557320203427], [88, 0.15000000000000002]],
           3: [[145, 0.857758242863828],  [88, 0.15000000000000002]]}
    
    ansBFS = {
        1: [68, 223, 12],
        2: [138, 87, 37],
        3: [148, 224, 13]
    }
    # Test PageRank
    for i in range(1,4):
        print("----------------------------------")
        print(f"Testcase: {i} for PageRank")
        result = test_page_rank(i*4, "distance")
        if result[0]['name'] == ansPageRank[i][0][0] \
            and round(result[0]['score'], 5) == round(ansPageRank[i][0][1],5) \
            and result[1]['name'] == ansPageRank[i][1][0]  \
            and round(result[1]['score'], 5) ==  round(ansPageRank[i][1][1],5):
            print(f"\tPageRank Test {i}: PASS")
        else:
            print(f"\tPageRank Test {i}: FAIL")
        if i < 3:
            tester.deleteGraph()
        print("----------------------------------")

        
    for j in range(1,4):
        # Test BFS
        print("----------------------------------")
        result = test_bfs(ansBFS[j][0], ansBFS[j][1])
        first_node = result[0]['path'][0]['name']
        last_node = result[0]['path'][-1]['name']

        node_count = len([i for i in result[0]['path'] if "name" in i])

        if first_node == ansBFS[j][0] and last_node == ansBFS[j][1] and node_count <= ansBFS[j][2]:
            print(f"\tBFS Test {i}: PASS")
        else:
            print(f"\tBFS Test {i}: FAIL")

        print("----------------------------------")
    tester.deleteGraph()
    tester.deleteData()
    print("\nTesting Complete: Note that the test cases are not exhaustive. You should run your own tests to ensure that your code is working correctly.")


if __name__ == "__main__":
    main()