import matplotlib.pyplot as plt
import numpy as np
from convexhull_quickhull_implementation import ConvexHull_QuickHull as ConvexHull
from matplotlib.animation import FuncAnimation

# Define the points A, B, C, D and the function to compute M for a given lambda
def get_point_M(lambda_value):
    return np.array([-2 + lambda_value, 3 - lambda_value])

# Function to determine if M is inside the square
def is_point_inside_square(lambda_value):
    # Define fixed points A, B, C, D
    points = np.array([
        [3, -3],  # A
        [3, 3],   # B
        [-3, -3], # C
        [-3, 3],  # D
    ])

    # Get the point M for the current lambda
    M = get_point_M(lambda_value)
    points = np.vstack([points, M])  # Add M to the list of points

    # Compute the convex hull
    hull = ConvexHull(points)

    # Check the number of points on the convex hull
    if len(hull.vertices) == 4:  # If 4 points are on the convex hull, M is inside
        return True
    return False

# Initialize the plot
fig, ax = plt.subplots(figsize=(6, 6))

# Define fixed points A, B, C, D
square_points = np.array([
    [3, -3],  # A
    [3, 3],   # B
    [-3, -3], # C
    [-3, 3],  # D
])

# Variable to track the open interval where M is inside the square
interval = None
last_inside = False  # Track the last state of inside/outside

# Animation function
def update(lambda_value):
    global interval, last_inside
    
    ax.clear()

    # Get the point M for the current lambda
    M = get_point_M(lambda_value)
    points = np.vstack([square_points, M])

    # Compute the convex hull
    hull = ConvexHull(points)

    # Plot square points and M
    ax.plot(square_points[:, 0], square_points[:, 1], 'bo', label="Square Points")
    ax.plot(M[0], M[1], 'ro', label=f"M (-2 + λ, 3 - λ)")

    # Plot the convex hull
    for simplex in hull.simplices:
        ax.plot(points[simplex, 0], points[simplex, 1], 'k-', label="Convex Hull" if simplex[0] == 0 else "")

    # Mark the vertices of the convex hull
    ax.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'go', label="Convex Hull Vertices")

    # Annotate points
    labels = ['A', 'B', 'C', 'D', 'M']
    for i, point in enumerate(points):
        ax.annotate(labels[i], (point[0] + 0.1, point[1] + 0.1))

    # Set labels and title
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Convex Hull for λ = {lambda_value:.2f}")

    # Highlight whether M is inside or outside
    inside = is_point_inside_square(lambda_value)
    if inside:
        ax.text(0, -4, "M is Inside the Square", color="green", fontsize=12, ha="center")
    else:
        ax.text(0, -4, "M is Outside the Square", color="red", fontsize=12, ha="center")

    # Track the interval where M is inside the square
    if inside:
        if interval is None:
            # Start a new open interval
            interval = [lambda_value, None]  # Only set the start of the interval
        last_inside = True
    else:
        if interval is not None and last_inside:
            # Close the current open interval and record it
            interval[1] = lambda_value  # Set the end of the interval
            # Print the interval once it is closed
            print(f"Interval where M is inside the square: λ ∈ ({interval[0]:.2f}, {interval[1]:.2f})")
            interval = None  # Reset the interval after it's closed
        last_inside = False

    ax.legend()
    ax.grid(True)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

# Generate animation
lambda_values = np.linspace(-10, 10, 200)  # Range of lambda values

# Stop the animation at lambda = 10
def stop_at_max(value):
    return value <= 10

ani = FuncAnimation(fig, update, frames=lambda_values, interval=50, repeat=False)

# Save or show animation
ani.save("lambda_point_M.gif", fps=60)

# Show the animation
plt.show()
