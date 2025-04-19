from Graph import Graph
import customtkinter as ctk
from CTkListbox import *

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq
import matplotlib.image as mpimg
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from PIL import Image

ctk.set_appearance_mode("system")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Djikstra's Algorithm")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.graph = Graph()

        self.frame = ctk.CTkScrollableFrame(self, width=200, height=600)
        self.frame.grid(row=0, column=0)

        self.node_label = ctk.CTkLabel(self.frame, text="Add Node")
        self.node_label.pack(padx=10, pady=10)

        self.node_entry = ctk.CTkEntry(self.frame, placeholder_text="Node Name")
        self.node_entry.pack(padx=10, pady=5)

        self.add_node_button = ctk.CTkButton(self.frame, text="Add", command=self.add_node)
        self.add_node_button.pack(padx=10, pady=10)

        self.div()

        self.node1_label = ctk.CTkLabel(self.frame, text="Add Edge")
        self.node1_label.pack(padx=10)

        self.node1_entry = ctk.CTkEntry(self.frame, placeholder_text="First node")
        self.node1_entry.pack(padx=10, pady=5)

        self.node2_entry = ctk.CTkEntry(self.frame, placeholder_text="Second node")
        self.node2_entry.pack(padx=10, pady=5)

        self.weight_entry = ctk.CTkEntry(self.frame, placeholder_text="Weight")
        self.weight_entry.pack(padx=10, pady=5)

        self.add_edge_button = ctk.CTkButton(self.frame, text="Add", command=self.add_edge)
        self.add_edge_button.pack(padx=10, pady=15)

        self.div()

        self.actions_label = ctk.CTkLabel(self.frame, text="Actions")
        self.actions_label.pack(padx=10)

        self.draw = ctk.CTkButton(self.frame, text="Visualize", command=self.draw)
        self.draw.pack(padx=10, pady=5)

        self.div()

        self.main_frame = ctk.CTkScrollableFrame(self, width=760, height=600)
        self.main_frame.grid(row=0, column=1)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.error = ctk.CTkLabel(self.main_frame, text="Warnings: ")
        self.error.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

        self.graph_frame = ctk.CTkFrame(master=self.main_frame, height=350, width=700, corner_radius=20, fg_color="#191d20")
        self.graph_frame.grid_propagate(False)
        self.graph_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=4)

        self.graph_label = ctk.CTkLabel(self.graph_frame, text="Graph Information", width=700)
        self.graph_label.pack(padx=10, pady=10)

        self.graph_display = ctk.CTkLabel(self.graph_frame, width=700, text="The graph is empty", anchor="nw", justify="left")
        self.graph_display.pack(padx=20, pady=10, anchor="w")

        self.graph_image = ctk.CTkLabel(self.graph_frame, text="")
        self.graph_image.pack(padx=20, pady=10, anchor="w")

    def add_node(self):
        self.error.configure(text="Warnings: ")
        node_name = self.node_entry.get()
        if node_name:
            self.graph.add_node(node_name)
            self.node_entry.delete(0, ctk.END)

            self.update_graph()
        else:
            self.error.configure(text="Warnings: Please enter a node name")

    def add_edge(self):
        self.error.configure(text="Warnings: ")
        node1 = self.node1_entry.get()
        node2 = self.node2_entry.get()
        weight = int(self.weight_entry.get())

        if node1 and node2 and weight:
            self.graph.add_edge(node1, node2, weight)
            self.node1_entry.delete(0, ctk.END)
            self.node2_entry.delete(0, ctk.END)
            self.weight_entry.delete(0, ctk.END)

            self.update_graph()
        elif not node1 or not node2:
            self.error.configure(text="Warnings: Add both nodes to the graph")
            return
        elif not int(weight):
            self.error.configure(text="Warnings: Add weight to the edge")
            return
        else:
            self.error.configure(text="Warnings: Please fill all fields")
            return

    def update_graph(self):
        self.graph_display.configure(text=str(self.graph.display()))
        self.graph_display.update()

    def div(self):
        self.divide = ctk.CTkLabel(self.frame, text="-----------------")
        self.divide.pack(padx=10, pady=10)

    def draw(self):
        plt.figure(figsize=(8, 6))
        G = nx.Graph()

        for node in self.graph.adjacencyList.keys():
            G.add_node(node)
        
        for node, neighbors in self.graph.adjacencyList.items():
            for neighbor, weight in neighbors:
                G.add_edge(node, neighbor, weight=weight)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.title("Graph Visualization")
        plt.savefig("graph.png")
        plt.close()

        image = Image.open("graph.png")
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(600, 400))

        self.graph_image_label.destroy() if hasattr(self, 'graph_image_label') else None
        self.graph_image_label = ctk.CTkLabel(self.graph_frame, image=ctk_image, text="")
        self.graph_image_label.image = ctk_image
        self.graph_image_label.pack(pady=10)

app = App()
app.mainloop()