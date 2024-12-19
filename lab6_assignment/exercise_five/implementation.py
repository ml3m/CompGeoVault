import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay, Voronoi, voronoi_plot_2d

def plot_triangulation_and_voronoi(points, ax1, ax2):
    # Perform Delaunay triangulation
    tri = Delaunay(points)
    ax1.triplot(points[:, 0], points[:, 1], tri.simplices, color='blue')
    ax1.plot(points[:, 0], points[:, 1], 'o', color='red')
    ax1.set_title("Delaunay Triangulation")

    # Annotate points with their coordinates
    for i, (x, y) in enumerate(points):
        ax1.annotate(f"({x:.1f}, {y:.1f})", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8, color="green")

    # Count edges in the triangulation
    edges = set()
    for simplex in tri.simplices:
        for i in range(3):
            edge = tuple(sorted([simplex[i], simplex[(i + 1) % 3]]))
            edges.add(edge)
    num_edges = len(edges)

    # Perform Voronoi diagram
    vor = Voronoi(points)
    voronoi_plot_2d(vor, ax=ax2, show_vertices=False, line_colors='orange', line_width=2)
    ax2.plot(points[:, 0], points[:, 1], 'o', color='red')
    ax2.set_title("Voronoi Diagram")

    # Annotate points with their coordinates
    for i, (x, y) in enumerate(points):
        ax2.annotate(f"({x:.1f}, {y:.1f})", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8, color="green")

    # Count half-line edges in the Voronoi diagram
    half_line_edges = sum(1 for region in vor.regions if -1 in region)

    return len(tri.simplices), num_edges, half_line_edges

# Example sets of points
M1 = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [0.5, 0.5], [0.5, 1.5]])
M2 = np.array([[0, 1], [1, 0], [1, -1], [1, 1], [0.5, 0.5], [-0.5, 1]])

# Plot and analyze M1
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
tri_faces_M1, edges_M1, half_edges_M1 = plot_triangulation_and_voronoi(M1, axes[0, 0], axes[0, 1])

# Plot and analyze M2
tri_faces_M2, edges_M2, half_edges_M2 = plot_triangulation_and_voronoi(M2, axes[1, 0], axes[1, 1])

# Display results
print(f"Set M1: Triangles = {tri_faces_M1}, Edges = {edges_M1}, Half-line Edges = {half_edges_M1}")
print(f"Set M2: Triangles = {tri_faces_M2}, Edges = {edges_M2}, Half-line Edges = {half_edges_M2}")

plt.tight_layout()
plt.show()
