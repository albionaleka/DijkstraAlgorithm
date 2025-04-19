# Dijkstra Algorithm

## Overview

**DijkstraAlgorithm** is a Python-based application that implements Dijkstra's shortest path algorithm with an interactive graphical user interface (GUI). It allows users to build graphs, set edge weights, and visualize the shortest path between nodes—perfect for learning and demonstrating the algorithm.

## Features

- ✅ Create nodes and edges with custom weights
- 🎨 Interactive GUI for visual graph manipulation
- 📍 Highlighted shortest path from source to destination
- 📚 Educational visualization of how Dijkstra's algorithm works

## Installation

### Prerequisites

- Python 3.x
- Recommended: virtual environment (venv)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/albionaleka/DijkstraAlgorithm.git
   cd DijkstraAlgorithm

2. **Create and activate a virtual environment (optional)**

    ```bash
    python -m venv venv
    source venv/bin/activate

3. **Install depencencies**
    ```bash
    pip install -r requirements.txt

## Usage

Launch the app with:

    ```bash
    python gui.py
    ```

Once the GUI is open, you can:

- 🟡 Click to add nodes on the canvas
- 🔗 Connect nodes to form edges and input their weights
- 🧭 Choose start and end nodes to calculate the shortest path
- 🌐 View the computed shortest path highlighted in the graph
