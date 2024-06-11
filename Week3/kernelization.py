import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

G = nx.erdos_renyi_graph(20, 0.15)
pos = nx.spring_layout(G)

def find_isolated(g):
    isolated = [i for i in g.nodes() if g.degree(i) == 0]
    return isolated

def find_pendant(g):
    pendant = [{"idx": i, "neighbour_idx": list(g.neighbors(i))[0]} for i in g.nodes() if g.degree(i) == 1]
    return pendant

def find_top(g, k):
    top = [{"idx": i, "degree": g.degree(i)} for i in g.nodes() if g.degree(i) > k]
    return top

def add_pendant(g):
    non_pendants = [node for node, degree in dict(g.degree()).items() if degree != 1]
    if non_pendants:
        node = non_pendants[0]
        neighbors = list(g.neighbors(node))
        if neighbors:
            for neighbor in neighbors:
                g.remove_edge(node, neighbor)
            pendant_neighbor = neighbors[0]
            g.add_edge(node, pendant_neighbor)

def remove_pendant(g):
    pendants = [node for node, degree in dict(g.degree()).items() if degree == 1]
    if pendants:
        node = pendants[0]
        pendant_neighbor = list(g.neighbors(node))[0]
        g.remove_edge(node, pendant_neighbor)
        other_node = next((n for n in g.nodes() if n != node and n != pendant_neighbor), None)
        if other_node:
            g.add_edge(pendant_neighbor, other_node)

def add_top(g, k):
    non_tops = [node for node, degree in dict(g.degree()).items() if degree <= k]
    if non_tops:
        node = non_tops[0]
        for _ in range(k + 1 - g.degree(node)):
            other_node = next((n for n in g.nodes() if n != node and not g.has_edge(node, n)), None)
            if other_node:
                g.add_edge(node, other_node)

def remove_top(g, k):
    tops = [node for node, degree in dict(g.degree()).items() if degree > k]
    if tops:
        node = tops[0]
        neighbors = list(g.neighbors(node))
        for _ in range(g.degree(node) - k):
            g.remove_edge(node, neighbors.pop())

def kernelization_and_visualization(g, k):
    isolated = find_isolated(g)
    pendants = find_pendant(g)
    tops = find_top(g, k)

    color_map = []
    for node in g.nodes():
        if node in isolated:
            color_map.append('gray')
        elif any(p['idx'] == node for p in pendants):
            color_map.append('blue')
        elif any(t['idx'] == node for t in tops):
            color_map.append('red')
        else:
            color_map.append('green')

    fig, ax = plt.subplots(figsize=(8, 6))
    pos.update(nx.spring_layout(g))
    nx.draw(g, pos, node_color=color_map, with_labels=True, edge_color='gray', node_size=500, font_size=10, ax=ax)
    return fig

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Kernelization")

        self.frame = Frame(self.root)
        self.frame.pack()

        self.canvas = None

        self.create_buttons()
        self.update_graph()

    def create_buttons(self):
        btn_add_pendant = Button(self.frame, text="Add Pendant", command=lambda: self.update_graph('add_pendant'))
        btn_remove_pendant = Button(self.frame, text="Remove Pendant",
                                    command=lambda: self.update_graph('remove_pendant'))
        btn_add_top = Button(self.frame, text="Add Top", command=lambda: self.update_graph('add_top'))
        btn_remove_top = Button(self.frame, text="Remove Top", command=lambda: self.update_graph('remove_top'))

        btn_add_pendant.grid(row=0, column=0)
        btn_remove_pendant.grid(row=0, column=1)
        btn_add_top.grid(row=0, column=2)
        btn_remove_top.grid(row=0, column=3)

    def update_graph(self, action=None):
        if action == 'add_pendant':
            add_pendant(G)
        elif action == 'remove_pendant':
            remove_pendant(G)
        elif action == 'add_top':
            add_top(G, 4)
        elif action == 'remove_top':
            remove_top(G, 4)

        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        fig = kernelization_and_visualization(G, 4)
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

root = Tk()
app = GraphApp(root)
root.mainloop()
