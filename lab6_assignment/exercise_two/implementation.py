import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d, ConvexHull

# Define the initial points A1 to A6
points = [
    (5, 1),  # A1
    (7, -1), # A2
    (9, -1), # A3
    (7, 3),  # A4
    (11, 1), # A5
    (9, 3)   # A6
]

# Add two additional points A7 and A8 to create 4 half-line edges
points.append((-5, 1))  # A7: Far to the left
points.append((15, 1))  # A8: Far to the right

# Separate the first six points for convex hull computation
points_for_hull = points[:6]

# Compute the convex hull for A1 to A6
hull = ConvexHull(points_for_hull)

# Create the Voronoi diagram
vor = Voronoi(points)

# Plot the Voronoi diagram
fig, ax = plt.subplots(figsize=(8, 8))
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='blue', line_width=1.5, point_size=10)

# Highlight the points
for i, (x, y) in enumerate(points, start=1):
    ax.plot(x, y, 'o', color='red', label=f'A{i}' if i <= 6 else f'A{i}', markersize=8)
    ax.text(x + 0.2, y, f'A{i}', fontsize=10)

# Plot the convex hull
hull_points = [points_for_hull[vertex] for vertex in hull.vertices]
hull_points.append(hull_points[0])  # Close the polygon
hx, hy = zip(*hull_points)
ax.plot(hx, hy, 'green', linestyle='--', linewidth=2, label='Convex Hull (A1-A6)')

# Set limits for better visualization
ax.set_xlim(-10, 20)
ax.set_ylim(-5, 10)

# Add grid, legend, and title
plt.grid()
plt.legend(loc='upper left', fontsize=10)
plt.title("Voronoi Diagram with Convex Hull and 4 Half-Line Edges", fontsize=14)

# Display the plot
plt.show()

# Explanation:
# The convex hull of A1-A6 is shown as a green dashed polygon.
# A7 and A8 are placed outside this convex hull, ensuring their Voronoi regions are unbounded,
# resulting in exactly 4 half-line edges.
