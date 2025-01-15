import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.spatial import Delaunay
import itertools

# Define the points
points_dict = {
    'A': (4, 7),
    'B': (7, 5),
    'C': (6, 1),
    'D': (4, 4),
    'E': (2, 1),
    'F': (1, 5)
}

# Convert to numpy array for Delaunay
points_array = np.array(list(points_dict.values()))
labels = list(points_dict.keys())

def plot_delaunay(ax, points, tri, point_labels, title, alpha=1.0):
    """Plot Delaunay triangulation"""
    ax.clear()
    
    # Plot points
    ax.scatter(points[:, 0], points[:, 1], color='blue')
    
    # Add labels
    for i, label in enumerate(point_labels):
        ax.annotate(label, (points[i, 0], points[i, 1]), 
                   xytext=(5, 5), textcoords='offset points')
    
    # Plot triangulation
    for simplex in tri.simplices:
        vertices = points[simplex]
        ax.plot(vertices[[0, 1], 0], vertices[[0, 1], 1], 'r-', alpha=alpha)
        ax.plot(vertices[[1, 2], 0], vertices[[1, 2], 1], 'r-', alpha=alpha)
        ax.plot(vertices[[2, 0], 0], vertices[[2, 0], 1], 'r-', alpha=alpha)
    
    ax.set_title(title)
    ax.grid(True)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)

def animate(frame):
    """Animation function"""
    if not hasattr(animate, 'ax1'):
        animate.ax1 = plt.subplot(131)
        animate.ax2 = plt.subplot(132)
        animate.ax3 = plt.subplot(133)
    
    # Calculate progress
    progress = (frame % 30) / 29
    
    # Full triangulation
    tri_full = Delaunay(points_array)
    plot_delaunay(animate.ax1, points_array, tri_full, labels, 
                 "Full Delaunay Triangulation", alpha=progress)
    
    # Two random 4-point subsets
    subset_indices1 = [0, 1, 2, 4]  # A, B, D, F
    subset_points1 = points_array[subset_indices1]
    subset_labels1 = [labels[i] for i in subset_indices1]
    tri_subset1 = Delaunay(subset_points1)
    plot_delaunay(animate.ax2, subset_points1, tri_subset1, subset_labels1,
                 "4-point Subset 1", alpha=progress)
    
    subset_indices2 = [1, 2, 3, 4]  # B, C, D, E
    subset_points2 = points_array[subset_indices2]
    subset_labels2 = [labels[i] for i in subset_indices2]
    tri_subset2 = Delaunay(subset_points2)
    plot_delaunay(animate.ax3, subset_points2, tri_subset2, subset_labels2,
                 "4-point Subset 2", alpha=progress)
    
    plt.tight_layout()

# Create figure
plt.close('all')
fig = plt.figure(figsize=(15, 5))

# Create animation
anim = FuncAnimation(fig, animate, frames=60, interval=100, repeat=True)

# Save as GIF
writer = PillowWriter(fps=10)
anim.save('delaunay_triangulation.gif', writer=writer)

plt.show()
