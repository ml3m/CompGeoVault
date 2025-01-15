import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from collections import defaultdict

def three_coloring(graph):
    """
    Colors the vertices of a graph using at most 3 colors such that 
    no two adjacent vertices share the same color.
    
    Parameters:
        graph (dict): A dictionary representing the adjacency list of the graph.
    
    Returns:
        dict: A dictionary mapping vertices to colors (0, 1, or 2).
    """
    vertex_colors = {}

    for vertex in graph:
        # Get the colors used by adjacent vertices
        used_colors = {vertex_colors[neighbor] for neighbor in graph[vertex] if neighbor in vertex_colors}
        
        # Assign the smallest available color
        for color in range(3):  # We only have 3 colors
            if color not in used_colors:
                vertex_colors[vertex] = color
                break

    return vertex_colors


def check_coloring_conditions(graph, coloring):
    """
    Checks if the coloring satisfies the condition that no two adjacent vertices
    share the same color.
    
    Parameters:
        graph (dict): The adjacency list of the graph.
        coloring (dict): A dictionary mapping vertices to colors.
    
    Returns:
        bool: True if the coloring satisfies the condition, False otherwise.
    """
    for vertex in graph:
        for neighbor in graph[vertex]:
            if coloring.get(vertex) == coloring.get(neighbor):
                return False  # Found an adjacent pair with the same color
    return True


def animate_graph(coords, edges, points, coloring, ax):
    """
    Animates the graph drawing: first drawing vertices, then edges, then coloring.

    Parameters:
        coords (dict): The dictionary of vertex coordinates.
        edges (list): The edges of the graph.
        points (list): The list of vertices.
        coloring (dict): The coloring of the vertices.
        ax (matplotlib axis): The axis to plot on.
    """
    color_map = ['red', 'green', 'blue']
    node_colors = ['gray' for _ in points]  # Initially set all nodes to gray
    pos = {node: coords[node] for node in points}
    
    # Step 1: Draw the points
    ax.scatter([coords[point][0] for point in points], [coords[point][1] for point in points], color='black', s=100)
    
    # Step 2: Animate edges one by one
    def animate_edges(i):
        ax.clear()
        # Draw vertices
        ax.scatter([coords[point][0] for point in points], [coords[point][1] for point in points], color='black', s=100)
        # Draw edges
        for edge in edges[:i]:
            ax.plot([coords[edge[0]][0], coords[edge[1]][0]], 
                    [coords[edge[0]][1], coords[edge[1]][1]], color='gray')
        ax.set_title(f"Edges drawn: {i}/{len(edges)}")

    # Step 3: Animate Coloring
    def animate_coloring(i):
        ax.clear()
        # Draw vertices
        ax.scatter([coords[point][0] for point in points], [coords[point][1] for point in points], color='black', s=100)
        # Draw edges
        for edge in edges:
            ax.plot([coords[edge[0]][0], coords[edge[1]][0]], 
                    [coords[edge[0]][1], coords[edge[1]][1]], color='gray')
        # Draw colored vertices
        for j, vertex in enumerate(points):
            ax.scatter(coords[vertex][0], coords[vertex][1], 
                       color=color_map[coloring[vertex]], s=100)
        ax.set_title(f"Step {i + 1}: Vertex Coloring")

    # Animation function to step through edges and coloring
    def update_frame(i):
        if i < len(edges):
            animate_edges(i)
        else:
            animate_coloring(i - len(edges))

    # Create the animation
    ani = animation.FuncAnimation(ax.figure, update_frame, frames=len(edges) + len(points), repeat=False, interval=1000)

    plt.show()


# Example Usage
if __name__ == "__main__":
    # Define the graph vertices and edges with uppercase letters as strings
    points = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    edges = [('B', 'A'), ('B', 'G'), ('B', 'F'), ('B', 'D'), ('B', 'E'), ('B', 'C'),
             ('C', 'E'), ('E', 'D'), ('D', 'F'), ('F', 'G'), ('G', 'A')]

    # Define custom (x, y) coordinates for each vertex
    coords = {
        'A': (3.03, 2.05),
        'B': (2.73, -1),
        'C': (0.7, -3.46),
        'D': (-2.73, -0.56),
        'E': (-1.59, -2.51),
        'F': (-2, 2),
        'G': (0.74, 3.24)
    }

    # Create adjacency list representation
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Apply the 3-coloring algorithm
    coloring = three_coloring(graph)

    print("_________________________________________________________________")
    # Print number of edges
    print(f"Number of edges: {len(edges)}")

    # Print vertex colors
    print("_________________________________________________________________")
    print("Vertex colors:")
    for vertex, color in coloring.items():
        print(f"Vertex {vertex}: Color {color}")

    # Check if the coloring conditions hold
    print("_________________________________________________________________")
    if check_coloring_conditions(graph, coloring):
        print("Condition holds: No two adjacent vertices have the same color.\n")
    else:
        print("Condition does not hold: Some adjacent vertices have the same color.\n")

    # Plot the graph with custom coordinates and animate
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_aspect('equal')

    animate_graph(coords, edges, points, coloring, ax)
