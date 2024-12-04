import matplotlib.pyplot as plt
import numpy as np
from convexhull_quickhull_implementation import ConvexHull_QuickHull as ConvexHull

# Define the points A, B, C, D and the function to compute M for a given lambda
def get_point_M(lambda_value):
    return np.array([-2 + lambda_value, 3 - lambda_value])

# Function to check how many points lie on the border of the convex hull and plot them
def points_on_convex_hull(lambda_value):
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

    # Get the set of vertices of the convex hull
    hull_vertices = set(hull.vertices)

    # Check how many of the original points (including M) are on the border
    on_border = 0
    for i in range(4):  # Only check the fixed points A, B, C, D
        if i in hull_vertices:
            on_border += 1

    # Check if M is on the border of the convex hull
    if 4 in hull_vertices:  # The index 4 corresponds to point M
        on_border += 1

    # Plot the points and convex hull
    plt.figure(figsize=(6, 6))

    # Plot all points
    plt.plot(points[:, 0], points[:, 1], 'bo', label='Points')

    # Plot the convex hull
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-', label='Convex Hull' if simplex[0] == 0 else "")

    # Mark the vertices of the convex hull
    plt.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'ro', label='Convex Hull Vertices')

    # Annotate points A, B, C, D, and M
    labels = ['A', 'B', 'C', 'D', 'M']
    for i, point in enumerate(points):
        plt.annotate(labels[i], (point[0] + 0.1, point[1] + 0.1))  # Adjust position to avoid overlap

    # Set labels and title
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Convex Hull for λ = {lambda_value}')
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.show()

    return on_border

# Example usage: Test for some lambda values
lambda_value = 2
count = points_on_convex_hull(lambda_value)
print("____________________________________________")
print(f"For λ = {lambda_value}, {count} points are on the convex hull.")
print("____________________________________________")
