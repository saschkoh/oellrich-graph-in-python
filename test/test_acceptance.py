from graph.core import GraphReader, GraphWriter

def run_test():
    # read graph from file
    graph = GraphReader("test/test-graphs/graph9.gra").read()
    # write graph to new file
    GraphWriter(graph, "test/graph9-copy.gra").write()
    # compare the two files
    with open("test/test-graphs/graph9.gra", "r", encoding="utf-8") as file1:
        with open("test/graph9-copy.gra", "r", encoding="utf-8") as file2:
            for line1, line2 in zip(file1, file2):
                assert line1 == line2
    print("Test passed")


if __name__ == "__main__":
    run_test()
