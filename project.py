import tkinter as tk
from tkinter import messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
import heapq

class MSTVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("MST Visualizer - Prim's & Kruskal's")
        self.graph = {}

        # UI Elements
        self.text_input = scrolledtext.ScrolledText(root, width=40, height=10)
        self.text_input.pack(pady=5)

        self.btn_load = tk.Button(root, text="Load Graph From Input", command=self.load_graph)
        self.btn_load.pack(pady=5)

        self.btn_prims = tk.Button(root, text="Run Prim's Algorithm", command=self.run_prims)
        self.btn_prims.pack(pady=5)

        self.btn_kruskals = tk.Button(root, text="Run Kruskal's Algorithm", command=self.run_kruskals)
        self.btn_kruskals.pack(pady=5)

        self.output_box = scrolledtext.ScrolledText(root, width=50, height=8, state='disabled')
        self.output_box.pack(pady=5)

    def load_graph(self):
        self.graph = {}
        input_text = self.text_input.get("1.0", tk.END).strip()
        for line in input_text.splitlines():
            try:
                u, v, w = line.strip().split()
                w = int(w)
                if u not in self.graph:
                    self.graph[u] = {}
                if v not in self.graph:
                    self.graph[v] = {}
                self.graph[u][v] = w
                self.graph[v][u] = w
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid line: {line}")
                return
        self.output_message("Graph loaded successfully.\n")
        self.draw_graph()

    def draw_graph(self, mst_edges=None, title="Graph"):
        G = nx.Graph()
        for node in self.graph:
            for neighbor, weight in self.graph[node].items():
                G.add_edge(node, neighbor, weight=weight)

        pos = nx.spring_layout(G, seed=42)
        labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        plt.figure(figsize=(6, 5))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=12)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        if mst_edges:
            mst_graph = nx.Graph()
            for u, v, w in mst_edges:
                mst_graph.add_edge(u, v, weight=w)
            nx.draw(mst_graph, pos, with_labels=True, edge_color='red', width=2, node_size=1000, font_size=12)

        plt.title(title)
        plt.show()

    def output_message(self, message):
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, message)
        self.output_box.see(tk.END)
        self.output_box.config(state='disabled')

    def run_prims(self):
        if not self.graph:
            messagebox.showwarning("Graph Missing", "Please load a graph first.")
            return
        mst_edges, total_weight, selection_order = self.prims_algorithm()
        self.output_message("Prim's Algorithm Node Selection Order:\n")
        for step, node in enumerate(selection_order):
            self.output_message(f"Step {step + 1}: Selected Node -> {node}\n")
        self.output_message(f"Total Weight of MST: {total_weight}\n\n")
        self.draw_graph(mst_edges, "Prim's Algorithm MST")

    def run_kruskals(self):
        if not self.graph:
            messagebox.showwarning("Graph Missing", "Please load a graph first.")
            return
        mst_edges, total_weight = self.kruskals_algorithm()
        messagebox.showinfo("Kruskal's Algorithm", f"Total Weight: {total_weight}")
        self.output_message(f"Kruskal's Algorithm Total Weight: {total_weight}\n\n")
        self.draw_graph(mst_edges, "Kruskal's Algorithm MST")

    def prims_algorithm(self):
        start_node = list(self.graph.keys())[0]
        visited = set()
        min_heap = [(0, start_node, None)]
        mst_edges = []
        total_weight = 0
        selection_order = []

        while min_heap:
            weight, node, parent = heapq.heappop(min_heap)
            if node not in visited:
                visited.add(node)
                selection_order.append(node)
                if parent is not None:
                    mst_edges.append((parent, node, weight))
                    total_weight += weight
                for neighbor, w in self.graph[node].items():
                    if neighbor not in visited:
                        heapq.heappush(min_heap, (w, neighbor, node))

        return mst_edges, total_weight, selection_order

    def find(self, parent, i):
        if parent[i] == i:
            return i
        parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        root_x = self.find(parent, x)
        root_y = self.find(parent, y)
        if rank[root_x] < rank[root_y]:
            parent[root_x] = root_y
        elif rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        else:
            parent[root_y] = root_x
            rank[root_x] += 1

    def kruskals_algorithm(self):
        edges = []
        seen = set()
        for node in self.graph:
            for neighbor, weight in self.graph[node].items():
                if (neighbor, node) not in seen:
                    edges.append((weight, node, neighbor))
                    seen.add((node, neighbor))

        edges.sort()
        parent = {node: node for node in self.graph}
        rank = {node: 0 for node in self.graph}
        mst_edges = []
        total_weight = 0

        for weight, u, v in edges:
            root_u = self.find(parent, u)
            root_v = self.find(parent, v)
            if root_u != root_v:
                mst_edges.append((u, v, weight))
                total_weight += weight
                self.union(parent, rank, root_u, root_v)

        return mst_edges, total_weight

if __name__ == "__main__":
    root = tk.Tk()
    app = MSTVisualizer(root)
    root.mainloop()
