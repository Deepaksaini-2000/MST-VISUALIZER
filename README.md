# MST-VISUALIZER
🔧 1. GUI Setup with Tkinter
MSTVisualizer class
Creates the main window and GUI components.

Allows:

Input of graph edges.

Button to load the graph.

Buttons to run Prim's and Kruskal's algorithms.

Text box to display algorithm output.

UI Elements
python

self.text_input = scrolledtext.ScrolledText(...)
self.btn_load = tk.Button(...)
self.output_box = scrolledtext.ScrolledText(...)
Used for user input, algorithm execution, and showing output.

📥 2. Graph Input & Parsing
load_graph() method
Reads the user input where each line has the format: u v w (nodes and edge weight).

Builds an adjacency list: self.graph = {} where each node maps to its neighbors and weights.

Checks for invalid input and shows error using messagebox.

🧭 3. Drawing the Graph
draw_graph() method
Uses networkx and matplotlib to visualize:

Original graph (edges in gray).

MST edges (highlighted in red if provided).

Uses spring_layout for nice spacing of nodes.

🌲 4. Prim's Algorithm
run_prims() + prims_algorithm()
Starts from any node.

Uses a min-heap (priority queue) to always pick the lightest edge leading to an unvisited node.

Tracks:

Visited nodes.

Selection order.

MST edges and total weight.

Visualizes the resulting MST and prints step-by-step selection.

🔗 5. Kruskal's Algorithm
run_kruskals() + kruskals_algorithm()
Creates a sorted list of all edges by weight.

Uses Union-Find (Disjoint Set Union) to detect cycles.

Adds edges in increasing weight order if they don’t form a cycle.

Functions:

find() — finds root of a node.

union() — merges two sets with rank optimization.

Shows MST and total weight in a popup and output box.

🎯 6. Main Entry Point
python
Copy
Edit
if __name__ == "__main__": ...
Launches the Tkinter window and app when script is run directly.

🧠 Example Input Format
A B 4
A C 2
B C 5
B D 10
C D 3
✅ Summary of Key Concepts
Tkinter for GUI.

networkx and matplotlib for graph visualization.

Prim’s Algorithm — Greedy approach with a priority queue.

Kruskal’s Algorithm — Greedy approach with sorting + union-find.

Graph represented as an adjacency list.

