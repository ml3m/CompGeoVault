import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d
import networkx as nx

def add_point_labels(points, ax):
    """Helper function to add coordinate labels to points"""
    for idx, point in enumerate(points):
        ax.annotate(f'({point[0]}, {point[1]})',
                   (point[0], point[1]),
                   xytext=(10, 10),
                   textcoords='offset points',
                   fontsize=8,
                   bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

def plot_delaunay(points, ax=None):
    if ax is None:
        ax = plt.gca()
    tri = Delaunay(points)
    ax.triplot(points[:, 0], points[:, 1], tri.simplices, color='blue', alpha=0.6, linewidth=1)
    ax.scatter(points[:, 0], points[:, 1], color='red', s=50, zorder=5)
    add_point_labels(points, ax)
    ax.set_title("Delaunay Triangulation", pad=10)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal', adjustable='box')

def plot_voronoi(points, ax=None):
    if ax is None:
        ax = plt.gca()
    
    # Calculate the bounds of the plot
    margin = 0.5
    x_min, y_min = points.min(axis=0) - margin
    x_max, y_max = points.max(axis=0) + margin
    
    # Create Voronoi diagram
    vor = Voronoi(points)
    
    # Plot using voronoi_plot_2d with custom styling
    voronoi_plot_2d(
        vor,
        ax=ax,
        show_vertices=True,
        point_size=50,
        line_colors='green',
        line_width=2,
        line_alpha=0.6,
        vertex_color='orange',
        vertex_size=20
    )
    
    add_point_labels(points, ax)
    
    # Set plot limits to focus on the relevant area
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    
    ax.set_title("Voronoi Diagram", pad=10)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal', adjustable='box')

def plot_mst(points, ax=None):
    if ax is None:
        ax = plt.gca()
    
    tri = Delaunay(points)
    edges = set()
    for simplex in tri.simplices:
        for i in range(3):
            for j in range(i + 1, 3):
                edge = tuple(sorted([simplex[i], simplex[j]]))
                edges.add(edge)
    
    graph = nx.Graph()
    for edge in edges:
        p1, p2 = points[edge[0]], points[edge[1]]
        weight = np.linalg.norm(p1 - p2)
        graph.add_edge(edge[0], edge[1], weight=weight)
    
    mst = nx.minimum_spanning_tree(graph)
    
    for edge in mst.edges(data=True):
        p1, p2 = points[edge[0]], points[edge[1]]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='purple', linewidth=2, alpha=0.7)
    
    ax.scatter(points[:, 0], points[:, 1], color='red', s=50, zorder=5)
    add_point_labels(points, ax)
    ax.set_title("Minimum Spanning Tree", pad=10)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect('equal', adjustable='box')

# Example usage
if __name__ == "__main__":
    # Define points as a NumPy array
    points = np.array([
        [3, 5],
        [6, 6],
        [6, 4],
        [9, 5],
        [9, 7],
    ])

    # Create figure with improved layout and more vertical space for labels
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
    fig.suptitle('Geometric Structures Visualization', fontsize=14, y=1.05)

    # Plot each visualization
    plot_delaunay(points, ax1)
    plot_voronoi(points, ax2)
    plot_mst(points, ax3)

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()
