import matplotlib.pyplot as plt
import numpy as np
from convexhull_quickhull_implementation import ConvexHull_QuickHull as ConvexHull
from matplotlib.animation import FuncAnimation

# Define the points A, B, C, D and the function to compute M for a given lambda
def get_point_M(lambda_value):
    return np.array([-2 + lambda_value, 3 - lambda_value])

# Function to determine if M is inside the square
def is_point_inside_square(lambda_value):
    points = np.array([
        [3, -3],  # A
        [3, 3],   # B
        [-3, -3], # C
        [-3, 3],  # D
    ])
    M = get_point_M(lambda_value)
    points = np.vstack([points, M])
    hull = ConvexHull(points)
    return len(hull.vertices) == 4

# Initialize the plot
fig, ax = plt.subplots(figsize=(8, 8))
square_points = np.array([
    [3, -3],  # A
    [3, 3],   # B
    [-3, -3], # C
    [-3, 3],  # D
])
interval = None
last_inside = False

# Animation function
def update(lambda_value):
    global interval, last_inside
    ax.clear()
    M = get_point_M(lambda_value)
    points = np.vstack([square_points, M])
    hull = ConvexHull(points)
    ax.plot(square_points[:, 0], square_points[:, 1], 'bo', label="Square Points")
    ax.plot(M[0], M[1], 'ro', label=f"M (-2 + λ, 3 - λ)")
    for simplex in hull.simplices:
        ax.plot(points[simplex, 0], points[simplex, 1], 'k-', label="Convex Hull" if simplex[0] == 0 else "")
    ax.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'go', label="Hull Vertices")
    labels = ['A', 'B', 'C', 'D', 'M']
    for i, point in enumerate(points):
        ax.annotate(labels[i], (point[0] + 0.15, point[1] + 0.15), fontsize=10)
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.set_title(f"Convex Hull for λ = {lambda_value:.2f}", fontsize=14)
    inside = is_point_inside_square(lambda_value)
    if inside:
        ax.text(0, -4.5, "M is Inside the Square", color="green", fontsize=12, ha="center")
    else:
        ax.text(0, -4.5, "M is Outside the Square", color="red", fontsize=12, ha="center")
    if inside:
        if interval is None:
            interval = [lambda_value, None]
        last_inside = True
    else:
        if interval is not None and last_inside:
            interval[1] = lambda_value
            print(f"Interval where M is inside the square: λ ∈ ({interval[0]:.2f}, {interval[1]:.2f})")
            interval = None
        last_inside = False
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')

lambda_values = np.linspace(-10, 10, 200)
ani = FuncAnimation(fig, update, frames=lambda_values, interval=50, repeat=False)
ani.save("lambda_point_M.gif", dpi=150, fps=60)
plt.show()
