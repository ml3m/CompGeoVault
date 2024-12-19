import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d, ConvexHull

# Define the points A, B, C
A_points = [(1 + i, i - 1) for i in range(6)]  # A0, A1, ..., A5
B_points = [(-i, i) for i in range(6)]         # B0, B1, ..., B5
C_points = [(0, i) for i in range(6)]          # C0, C1, ..., C5

# Combine all points
points = A_points + B_points + C_points

# Create Voronoi diagram
vor = Voronoi(points)

# Function to find infinite half-lines in the Voronoi diagram
def count_half_lines(vor):
    half_lines_count = 0
    # Voronoi vertices and ridge points
    for ridge in vor.ridge_vertices:
        if -1 in ridge:  # If one of the vertices is -1, the ridge is infinite
            half_lines_count += 1
    return half_lines_count

# Calculate the number of half-lines
half_lines = count_half_lines(vor)

# Output the number of half-lines
print(f"Number of half-lines: {half_lines}")

# Plot the Voronoi diagram
fig, ax = plt.subplots(figsize=(10, 10))
voronoi_plot_2d(vor, ax=ax, show_vertices=False)

# Plot the original points
points_np = np.array(points)
ax.scatter(points_np[:, 0], points_np[:, 1], color='red', label='Points')

# Label points
for i, point in enumerate(points):
    ax.text(point[0] + 0.1, point[1] + 0.1, f'{i}', fontsize=12)

# Set labels and show the plot
ax.set_title("Voronoi Diagram")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.legend()
plt.grid(True)
plt.show()
