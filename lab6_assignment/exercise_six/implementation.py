import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.spatial import Delaunay

# Define the base points
A = np.array([1, -1])
B = np.array([-1, 1])
C = np.array([2, -1])
D = np.array([1, 1])
E = np.array([0, 2])

def compute_triangulation(lambda_value):
    # Define M based on lambda
    M = np.array([1, lambda_value])
    points = np.array([A, B, C, D, E, M])

    # Perform Delaunay triangulation
    delaunay = Delaunay(points)
    triangles = delaunay.simplices

    # Extract edges
    edges = set()
    for tri in triangles:
        for i in range(3):
            edge = tuple(sorted((tri[i], tri[(i + 1) % 3])))
            edges.add(edge)

    return points, delaunay, len(triangles), len(edges)

def update_plot(val):
    lambda_value = slider_lambda.val
    points, delaunay, num_triangles, num_edges = compute_triangulation(lambda_value)

    # Update plot
    ax.clear()
    ax.triplot(points[:, 0], points[:, 1], delaunay.simplices, color='blue')
    ax.scatter(points[:, 0], points[:, 1], color='red', zorder=5)

    # Label the points
    labels = ["A", "B", "C", "D", "E", "M"]
    for i, label in enumerate(labels):
        ax.text(points[i, 0] + 0.1, points[i, 1], label, fontsize=12, color='black')

    ax.set_title(f"Triangulation with λ = {lambda_value:.2f}\nTriangles: {num_triangles}, Edges: {num_edges}")
    ax.set_aspect('equal', adjustable='box')
    plt.draw()

# Initial setup
initial_lambda = 0.5
points, delaunay, num_triangles, num_edges = compute_triangulation(initial_lambda)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.2)

# Initial plot
ax.triplot(points[:, 0], points[:, 1], delaunay.simplices, color='blue')
ax.scatter(points[:, 0], points[:, 1], color='red', zorder=5)
labels = ["A", "B", "C", "D", "E", "M"]
for i, label in enumerate(labels):
    ax.text(points[i, 0] + 0.1, points[i, 1], label, fontsize=12, color='black')
ax.set_title(f"Triangulation with λ = {initial_lambda:.2f}\nTriangles: {num_triangles}, Edges: {num_edges}")
ax.set_aspect('equal', adjustable='box')

# Add slider
ax_lambda = plt.axes([0.25, 0.1, 0.65, 0.03])  # [left, bottom, width, height]
slider_lambda = Slider(ax_lambda, 'λ', -10.0, 10.0, valinit=initial_lambda)

# Attach the update function to the slider
slider_lambda.on_changed(update_plot)

# Show the plot
plt.show()
