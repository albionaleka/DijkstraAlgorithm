# from Graph import Graph
import customtkinter as ctk
from CTkListbox import *

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq

from PIL import Image

ctk.set_appearance_mode("system")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dijkstra's Algorithm")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.graph = nx.MultiDiGraph()
        self.animation_after_id = None  # Initialize animation timer ID

        self.frame = ctk.CTkScrollableFrame(self, width=200, height=600)
        self.frame.grid(row=0, column=0)

        self.node_label = ctk.CTkLabel(self.frame, text="Add Node 📍", font=("Verdana", 14), text_color="white")
        self.node_label.pack(padx=10, pady=10)

        self.node_entry = ctk.CTkEntry(self.frame, placeholder_text="Node Name")
        self.node_entry.pack(padx=10, pady=5)

        self.add_node_button = ctk.CTkButton(self.frame, text="Add", command=self.add_node)
        self.add_node_button.pack(padx=10, pady=10)

        self.div()

        self.node1_label = ctk.CTkLabel(self.frame, text="Add Edge 📏", font=("Verdana", 14), text_color="white")
        self.node1_label.pack(padx=10)

        self.node1_entry = ctk.CTkEntry(self.frame, placeholder_text="First node")
        self.node1_entry.pack(pady=5)

        self.node2_entry = ctk.CTkEntry(self.frame, placeholder_text="Second node")
        self.node2_entry.pack(pady=5)

        self.weight_entry = ctk.CTkEntry(self.frame, placeholder_text="Weight")
        self.weight_entry.pack(pady=5)

        self.add_edge_button = ctk.CTkButton(self.frame, text="Add", command=self.add_edge)
        self.add_edge_button.pack(padx=10, pady=5)

        self.add_bidirectional_button = ctk.CTkButton(self.frame, text="Add Two-Way", command=self.add_bidirectional_edge)
        self.add_bidirectional_button.pack(padx=10, pady=10)

        self.div()

        self.actions_label = ctk.CTkLabel(self.frame, text="Actions ⚙", font=("Verdana", 15), text_color="white")
        self.actions_label.pack(padx=10)

        self.visualize = ctk.CTkButton(self.frame, text="Visualize", command=self.draw)
        self.visualize.pack(padx=10, pady=10)

        self.start = ctk.CTkEntry(self.frame, placeholder_text="Start Node")
        self.start.pack(padx=10, pady=5)

        self.end = ctk.CTkEntry(self.frame, placeholder_text="End Node")
        self.end.pack(padx=10, pady=5)

        self.dijkstra = ctk.CTkButton(self.frame, text="Find Path", command=self.run_dijkstra)
        self.dijkstra.pack(padx=10, pady=5)

        self.animate_button = ctk.CTkButton(self.frame, text="Animate Path", command=self.animate_dijkstra)
        self.animate_button.pack(padx=10, pady=5)

        self.div()

        self.main_frame = ctk.CTkScrollableFrame(self, width=760, height=600)
        self.main_frame.grid(row=0, column=1)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.graph_label = ctk.CTkLabel(self.main_frame, text="Graph Information 📈", width=700, font=("Verdana", 20), text_color="white")
        self.graph_label.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        self.error = ctk.CTkLabel(self.main_frame, text="Warnings: ", font=("Verdana", 14), text_color="#ff2828")
        self.error.grid(row=1, column=0, padx=15, pady=10, columnspan=4, sticky="w")

        self.graph_frame = ctk.CTkFrame(master=self.main_frame, height=350, width=700, corner_radius=20, fg_color="#191d20")
        self.graph_frame.grid_propagate(False)
        self.graph_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=4)

        self.graph_display = ctk.CTkLabel(self.graph_frame, width=700, text="The graph is empty", anchor="nw", justify="left")
        self.graph_display.pack(padx=20, pady=10, anchor="w")

        self.result = ctk.CTkLabel(self.graph_frame, text="")
        self.result.pack(padx=20, anchor="w")

        self.graph_image = ctk.CTkLabel(self.graph_frame, text="")
        self.graph_image.pack(padx=20)

    def add_node(self):
        self.error.configure(text="Warnings: ")
        node_name = self.node_entry.get().upper()
        if node_name:
            self.graph.add_node(node_name)
            self.node_entry.delete(0, ctk.END)

            self.update_graph_display()
        else:
            self.error.configure(text="Warnings: Please enter a node name")

    def add_edge(self):
        self.error.configure(text="Warnings: ")
        node1 = self.node1_entry.get().upper()
        node2 = self.node2_entry.get().upper()
        weight_str = self.weight_entry.get()

        if node1 and node2 and weight_str:
            try:
                weight = int(weight_str)
                if weight <= 0:
                    raise ValueError("Weight must be positive")
            except ValueError as e:
                self.error.configure(text=f"Warnings: {e}")
                return

            if node1 not in self.graph.nodes or node2 not in self.graph.nodes:
                self.error.configure(text="Warnings: Add both nodes to the graph first")
                return

            self.graph.add_edge(node1, node2, weight=weight)

            self.node1_entry.delete(0, ctk.END)
            self.node2_entry.delete(0, ctk.END)
            self.weight_entry.delete(0, ctk.END)

            self.update_graph_display()
        else:
            self.error.configure(text="Warnings: Please fill all fields")
            return

    def add_bidirectional_edge(self):
        self.error.configure(text="Warnings: ")
        node1 = self.node1_entry.get().upper()
        node2 = self.node2_entry.get().upper()
        weight_str = self.weight_entry.get()

        if node1 and node2 and weight_str:
            try:
                weight = int(weight_str)
                if weight <= 0:
                    raise ValueError("Weight must be positive")
            except ValueError as e:
                self.error.configure(text=f"Warnings: {e}")
                return

            if node1 not in self.graph.nodes or node2 not in self.graph.nodes:
                self.error.configure(text="Warnings: Add both nodes to the graph first")
                return

            self.graph.add_edge(node1, node2, weight=weight)
            self.graph.add_edge(node2, node1, weight=weight)

            self.node1_entry.delete(0, ctk.END)
            self.node2_entry.delete(0, ctk.END)
            self.weight_entry.delete(0, ctk.END)

            self.update_graph_display()
        else:
            self.error.configure(text="Warnings: Please fill all fields")
            return

    def update_graph_display(self):
        display_text = ""
        for node, neighbors in self.graph.adjacency():
            display_text += f"{node}: "
            neighbor_weights = []
            for neighbor, edges in neighbors.items():
                for _, data in edges.items():
                    neighbor_weights.append(f"{neighbor}({data.get('weight', 1)})")
            display_text += ", ".join(neighbor_weights) + "\n\n"
        self.graph_display.configure(text=display_text if display_text else "The graph is empty")

    def div(self):
        self.divide = ctk.CTkLabel(self.frame, text="-----------------")
        self.divide.pack(padx=10, pady=10)

    def cleanup_animation(self):
        if hasattr(self, 'animation_after_id') and self.animation_after_id is not None:
            self.after_cancel(self.animation_after_id)
            self.animation_after_id = None

    def draw(self):
        if not self.graph.nodes:
            self.error.configure(text="Warnings: The graph is empty. Add nodes and edges to visualize.")
            return

        self.cleanup_animation()

        pos = nx.spring_layout(self.graph)
        plt.figure(figsize=(8, 6))

        nx.draw_networkx_nodes(self.graph, pos, node_color='skyblue', node_size=2000)
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight='bold')

        nx.draw_networkx_edges(
            self.graph,
            pos,
            edge_color='gray',
            width=1,
            arrows=True,
            arrowsize=20,
            node_size=2000,
            connectionstyle='arc3, rad=0.1'
        )
        
        edge_labels = {(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)

        plt.axis('off')
        plt.tight_layout()
        plt.savefig("graph.png")
        plt.close()

        image = Image.open("graph.png")
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(600, 400))

        if hasattr(self, 'graph_image_label'):
            self.graph_image_label.destroy()
        self.graph_image_label = ctk.CTkLabel(self.graph_frame, image=ctk_image, text="")
        self.graph_image_label.image = ctk_image
        self.graph_image_label.pack(pady=10)

    def run_dijkstra(self):
        self.cleanup_animation()
        start_node = self.start.get().upper()
        end_node = self.end.get().upper()

        if not start_node or not end_node:
            self.error.configure(text="Warnings: Please enter start and end nodes.")
            return

        if start_node not in self.graph.nodes or end_node not in self.graph.nodes:
            self.error.configure(text="Warnings: Start or end node does not exist in the graph.")
            return

        distances, previous_nodes = self.dijkstra_algorithm(start_node)
        path = self.get_shortest_path(previous_nodes, start_node, end_node)
        self.shortest_path = path

        if path:
            shortest_distance = distances.get(end_node, float('inf'))
            self.result.configure(text=f"Shortest Path: {' ➡ '.join(path)}, Distance: {shortest_distance}")
            
            pos = nx.spring_layout(self.graph)
            plt.figure(figsize=(8, 6))

            nx.draw_networkx_nodes(self.graph, pos, node_color='lightgray', node_size=2000)
            nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight='bold')

            nx.draw_networkx_edges(
                self.graph,
                pos,
                edge_color='lightgray',
                width=1,
                arrows=True,
                arrowsize=20,
                node_size=2000,
                connectionstyle='arc3, rad=0.1'
            )

            edge_labels = {(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)}
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)

            path_edges = list(zip(path[:-1], path[1:]))
            if path_edges:
                nx.draw_networkx_nodes(self.graph, pos, 
                                     nodelist=path,
                                     node_color='skyblue',
                                     node_size=2000)
                
                nx.draw_networkx_edges(
                    self.graph,
                    pos,
                    edgelist=path_edges,
                    edge_color='red',
                    width=3,
                    arrows=True,
                    arrowsize=20,
                    node_size=2000,
                    connectionstyle='arc3, rad=0.1'
                )
            
            plt.axis('off')
            plt.tight_layout()
            plt.savefig("graph.png")
            plt.close()
            
            image = Image.open("graph.png")
            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(600, 400))
            
            if hasattr(self, 'graph_image_label'):
                self.graph_image_label.destroy()
            self.graph_image_label = ctk.CTkLabel(self.graph_frame, image=ctk_image, text="")
            self.graph_image_label.image = ctk_image
            self.graph_image_label.pack(pady=10)
        else:
            self.result.configure(text="No path found between the specified nodes.")

    def animate_dijkstra(self):
        if not self.graph.nodes:
            self.error.configure(text="Warnings: The graph is empty. Add nodes and edges to visualize.")
            return

        self.cleanup_animation()
        start_node = self.start.get().upper()
        end_node = self.end.get().upper()

        if not start_node or not end_node:
            self.error.configure(text="Warnings: Please enter start and end nodes.")
            return

        if start_node not in self.graph.nodes or end_node not in self.graph.nodes:
            self.error.configure(text="Warnings: Start or end node does not exist in the graph.")
            return

        distances, previous_nodes = self.dijkstra_algorithm(start_node)
        path = self.get_shortest_path(previous_nodes, start_node, end_node)
        self.shortest_path = path

        if not path:
            self.result.configure(text="No path found between the specified nodes.")
            return

        shortest_distance = distances.get(end_node, float('inf'))
        self.result.configure(text=f"Shortest Path: {' ➡ '.join(path)}, Distance: {shortest_distance}")

        fig, ax = plt.subplots(figsize=(7, 7))
        pos = nx.spring_layout(self.graph)

        def update(frame):
            ax.clear()
            
            nx.draw_networkx_nodes(self.graph, pos, node_color='lightgray', 
                                 node_size=2000, ax=ax)
            nx.draw_networkx_labels(self.graph, pos, font_size=10, 
                                  font_weight='bold', ax=ax)
            
            nx.draw_networkx_edges(
                self.graph,
                pos,
                edge_color='lightgray',
                width=1,
                arrows=True,
                arrowsize=20,
                node_size=2000,
                connectionstyle='arc3, rad=0.1'
            )

            edge_labels = {(u, v): d['weight'] for u, v, d in self.graph.edges(data=True)}
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels,
                                       font_size=8)
            
            if frame > 0:
                current_path = path[:frame+1]
                
                nx.draw_networkx_nodes(self.graph, pos, 
                                     nodelist=current_path,
                                     node_color='skyblue',
                                     node_size=2000, ax=ax)
                
                if frame < len(path):
                    nx.draw_networkx_nodes(self.graph, pos,
                                         nodelist=[path[frame]],
                                         node_color='red',
                                         node_size=2000, ax=ax)
                
                path_edges = list(zip(current_path[:-1], current_path[1:]))
                if path_edges:
                    nx.draw_networkx_edges(
                        self.graph,
                        pos,
                        edgelist=path_edges,
                        edge_color='red',
                        width=3,
                        arrows=True,
                        arrowsize=20,
                        node_size=2000,
                        connectionstyle='arc3, rad=0.1'
                    )
            
            ax.axis('off')
            return ax,

        anim = animation.FuncAnimation(fig, update, frames=len(path)+1, interval=2500, blit=False)
        anim.save('animation.gif', writer='pillow')
        plt.close()

        image = Image.open("animation.gif")
        frames = []
        try:
            while True:
                frames.append(ctk.CTkImage(light_image=image.copy(), 
                                         dark_image=image.copy(),
                                         size=(600, 400)))
                image.seek(len(frames))
        except EOFError:
            pass

        if hasattr(self, 'graph_image_label'):
            self.graph_image_label.destroy()

        self.graph_image_label = ctk.CTkLabel(self.graph_frame, image=frames[0], text="")
        self.graph_image_label.image = frames
        self.graph_image_label.pack(pady=10)

        self.update_frame(0, frames)

    def update_frame(self, frame_idx=0, frames=None):
        if hasattr(self, 'graph_image_label'):
            self.graph_image_label.configure(image=frames[frame_idx])
            frame_idx = (frame_idx + 1) % len(frames)
            self.animation_after_id = self.after(500, lambda: self.update_frame(frame_idx, frames))

    def dijkstra_algorithm(self, start_node):
        distances = {node: float('inf') for node in self.graph.nodes}
        distances[start_node] = 0
        priority_queue = [(0, start_node)]
        previous_nodes = {node: None for node in self.graph.nodes}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor in self.graph.neighbors(current_node):
                for _, data in self.graph.get_edge_data(current_node, neighbor).items():
                    weight = data.get('weight', 1)
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(priority_queue, (distance, neighbor))

        return distances, previous_nodes

    def get_shortest_path(self, previous_nodes, start_node, end_node):
        path = []
        current = end_node

        if end_node not in previous_nodes:
            return []

        if previous_nodes[end_node] is None and end_node != start_node:
            return []

        while current is not None:
            path.append(current)
            current = previous_nodes.get(current)

        path = path[::-1]

        if path and path[0] == start_node and path[-1] == end_node:
            return path
        return []

app = App()
app.mainloop()