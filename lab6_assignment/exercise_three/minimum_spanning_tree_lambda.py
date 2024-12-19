import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import pdist, squareform
import networkx as nx

# Fixed points
points = {
    'A': np.array([1, 6]),
    'B': np.array([1, 1]),
    'C': np.array([-4, 7]),
    'D': np.array([6, 7]),
    'E': np.array([1, -1]),
    'F': np.array([5, 3]),
    'P': np.array([-2, 3])
}

def get_mst(points_array):
    # Calculate pairwise distances
    distances = pdist(points_array)
    # Convert to square matrix
    dist_matrix = squareform(distances)
    # Calculate minimum spanning tree
    mst = minimum_spanning_tree(dist_matrix)
    return mst.toarray()

def update(frame):
    plt.clf()
    
    # Current position of Q
    Q = np.array([frame - 2, 3])
    
    # Combine all points including current Q position
    current_points = list(points.values()) + [Q]
    points_array = np.array(current_points)
    
    # Get MST for current configuration
    mst = get_mst(points_array)
    
    # Plot points
    plt.scatter(points_array[:, 0], points_array[:, 1], c='blue')
    
    # Plot MST edges
    for i in range(len(mst)):
        for j in range(len(mst)):
            if mst[i, j] > 0:
                plt.plot([points_array[i, 0], points_array[j, 0]],
                        [points_array[i, 1], points_array[j, 1]], 'r-')
    
    # Add labels
    labels = list(points.keys()) + ['Q']
    for i, label in enumerate(labels):
        plt.annotate(label, (points_array[i, 0], points_array[i, 1]),
                    xytext=(5, 5), textcoords='offset points')
    
    # Calculate total MST length
    total_length = np.sum(mst)
    plt.title(f'λ = {frame:.1f}, Total MST Length = {total_length:.2f}')
    
    plt.grid(True)
    plt.xlim(-5, 7)
    plt.ylim(-2, 8)

# Create the animation
fig = plt.figure(figsize=(10, 8))
ani = FuncAnimation(fig, update, frames=np.linspace(0, 7, 71),
                   interval=100, repeat=True)

plt.show()
