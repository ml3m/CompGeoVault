import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def create_triangulation():
    # Create points in the plane
    points = {
        'A': (0, 0),
        'B': (2, 0),
        'C': (4, 0),
        'D': (1, 2),
        'E': (3, 2),
        'F': (2, 4),
        'G': (2, 1)  # Internal point
    }
    
    # Define edges of the triangulation
    edges = [
        ('A', 'B'), ('B', 'C'),  # Bottom edges
        ('A', 'D'), ('B', 'D'), ('B', 'E'), ('C', 'E'),  # Middle edges
        ('D', 'F'), ('E', 'F'),  # Upper edges
        ('D', 'G'), ('E', 'G'), ('B', 'G')  # Internal edges
    ]
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes with positions
    for node, pos in points.items():
        G.add_node(node, pos=pos)
    
    # Add edges
    G.add_edges_from(edges)
    
    return G, points

def visualize_triangulation(G, points, colors=None):
    plt.figure(figsize=(10, 8))
    
    # Draw edges
    nx.draw_networkx_edges(G, points, edge_color='black')
    
    # Draw nodes
    if colors:
        node_colors = [colors.get(node, 'white') for node in G.nodes()]
    else:
        node_colors = ['white'] * len(G.nodes())
    
    nx.draw_networkx_nodes(G, points, node_color=node_colors, 
                          node_size=500, edgecolors='black')
    
    # Add labels
    nx.draw_networkx_labels(G, points)
    
    plt.axis('equal')
    plt.grid(True)
    plt.title("Triangulation with 11 edges")
    
def three_color_graph(G):
    colors = {}
    available_colors = ['red', 'green', 'blue']
    
    for node in G.nodes():
        # Get colors of neighbors
        neighbor_colors = {colors.get(neighbor) for neighbor in G.neighbors(node)}
        
        # Find first available color
        for color in available_colors:
            if color not in neighbor_colors:
                colors[node] = color
                break
    
    return colors

# Create and visualize the triangulation
G, points = create_triangulation()
visualize_triangulation(G, points)

# Compute and visualize 3-coloring
colors = three_color_graph(G)
visualize_triangulation(G, points, colors)

# Verify number of edges
print(f"Number of edges: {G.number_of_edges()}")
print("3-coloring:", colors)

# Display the plots
plt.show()
