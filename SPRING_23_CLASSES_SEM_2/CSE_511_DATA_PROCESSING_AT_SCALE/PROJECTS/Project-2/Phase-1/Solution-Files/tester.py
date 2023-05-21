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

            if (num_nodes == 42):
                print("\tCount of Edges is correct: PASS")
            else:
                print("\tCount of Edges is incorrect: FAIL")

            if (num_edges == 1530):
                print("\tCount of Edges is correct: PASS")
            else:
                print("\tCount of Edges is incorrect: FAIL")


def test_page_rank(max_iter, prop_name):
    """
    Test to see if PageRank implemented in interface is working
        1. Run a query to perform PageRank
        2. Compare the results with the expected results
    """


    conn = interface.Interface("neo4j://localhost:7687", "neo4j", "project2phase1")
    result = conn.pagerank(max_iter, prop_name)

    return result


def test_bfs(start_node, last_node):
    """
    Test to see if BFS implemeted in interface is working
        1. Run a query to perform a BFS
        2. Compare the results with the expected results
    """

    print("Testing if BFS is working")

    conn = interface.Interface("neo4j://localhost:7687", "neo4j", "project2phase1")
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
    tester = TesterConnect("neo4j://localhost:7687", "neo4j", "project2phase1")
    tester.test_data_loaded()
    tester.close()

    # Test PageRank
    print("Testing if PageRank is working")
    result = test_page_rank(20, "distance")
    if result[0]['name'] == 159 and round(result[0]['score'], 5) == 3.22825 and result[1]['name'] == 59 and round(result[1]['score'], 5) == 0.18247:
        print("\tPageRank Test 1: PASS")
    else:
        print("\tPageRank Test 1: FAIL")

    # Test BFS
    result = test_bfs(159, 212)
    first_node = result[0]['path'][0]['name']
    last_node = result[0]['path'][-1]['name']

    node_count = len([i for i in result[0]['path'] if "name" in i])

    if first_node == 159 and last_node == 212:
        print("\tBFS Test 2: PASS")
    else:
        print("\tBFS Test 2: FAIL")

    print("----------------------------------")

    print("\nTesting Complete: Note that the test cases are not exhaustive. You should run your own tests to ensure that your code is working correctly.")


if __name__ == "__main__":
    main()