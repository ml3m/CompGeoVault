import matplotlib.pyplot as plt
from convexhull_quickhull_implementation import ConvexHull_QuickHull as ConvexHull
import numpy as np

# Define user-defined points
points = np.array([
    [30, 60],
    [15, 25],
    [0, 30],
    [70, 30],
    [50, 40],
    [50, 10],
    [20, 0],
    [55, 20]
])

# Compute the convex hull
hull = ConvexHull(points)

# Plot the points with larger markers and a distinct color
plt.figure(figsize=(8, 6))  # Larger figure for better clarity
plt.scatter(points[:, 0], points[:, 1], color='blue', s=100, label='User Defined Points', zorder=5)

# Plot the convex hull with a thicker line and a contrasting color
for simplex in hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'r-', linewidth=2, zorder=3)

# Highlight the vertices of the convex hull with red markers
plt.scatter(points[hull.vertices, 0], points[hull.vertices, 1], color='red', s=150, label='Convex Hull Vertices', edgecolors='black', zorder=6)

# Annotate the points with their coordinates for clarity
for i, (x, y) in enumerate(points):
    plt.text(x + 1, y + 1, f'({x},{y})', fontsize=9, color='black', zorder=7)

# Set labels, title, and grid
plt.xlabel('X-axis', fontsize=12)
plt.ylabel('Y-axis', fontsize=12)
plt.title('Convex Hull Visualization with QuickHull', fontsize=14)
plt.legend()

# Display grid lines and adjust limits for better clarity
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xlim(-5, 75)
plt.ylim(-5, 75)

# Show the plot
plt.show()
