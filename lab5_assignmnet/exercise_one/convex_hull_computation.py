import matplotlib.pyplot as plt
from convexhull_quickhull_implementation import ConvexHull_QuickHull as ConvexHull
import numpy as np

# Define your user-defined points as a list of tuples or an array
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

# Plot the points
plt.plot(points[:, 0], points[:, 1], 'o', label='User Defined Points')

# Plot the convex hull
for simplex in hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

# Optional: Mark the vertices of the convex hull
plt.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'ro', label='Convex Hull Vertices')

# Set labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Convex Hull Visualization')
plt.legend()

# Display the plot
plt.show()
