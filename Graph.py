class Graph:
    def __init__(self):
        self.adjacencyList = {}

    def add_node(self, node):
        if node not in self.adjacencyList:
            self.adjacencyList[node] = []

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)

        self.adjacencyList[node1].append((node2, weight))
        self.adjacencyList[node2].append((node1, weight))

    def remove_edge(self, node1, node2):
        if node1 in self.adjacencyList and node2 in self.adjacencyList:
            self.adjacencyList[node1].remove(node2)
            self.adjacencyList[node2].remove(node1)

    def remove_node(self, node):
        if node in self.adjacencyList:
            for neighbor in self.adjacencyList[node]:
                self.adjacencyList[neighbor].remove(node)

            del self.adjacencyList[node]

    def display(self):
        graph = ""
        for node, neighbors in self.adjacencyList.items():
            graph += f"{node}: "
            graph += ", ".join(f"{neighbor}({weight})" for neighbor, weight in neighbors)
            graph += "\n"
        return graph