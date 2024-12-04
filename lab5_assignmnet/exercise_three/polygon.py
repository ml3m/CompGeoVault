import matplotlib.pyplot as plt
from math import atan2

def compute_polygon(points):
    """
    Compute a simple polygon that includes all points by sorting them
    in counter-clockwise order around the centroid.
    """
    # Calculate the centroid of the points
    cx = sum(x for x, y in points) / len(points)
    cy = sum(y for x, y in points) / len(points)

    # Sort points by angle with respect to the centroid
    points.sort(key=lambda p: atan2(p[1] - cy, p[0] - cx))
    return points

def plot_polygon(points, polygon):
    """
    Plot the points and the computed polygon.
    """
    # Plot all points
    x, y = zip(*points)
    plt.scatter(x, y, label="Points", color="blue")

    # Plot the polygon
    polygon.append(polygon[0])  # Ensure the polygon is closed
    px, py = zip(*polygon)
    plt.plot(px, py, label="Polygon", color="green")

    # Customize and show the plot
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Polygon Containing All Points")
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    # Example points
    points = [(4, 2), (7, -1), (3, -5), (-3, 6), (-4, 4), (-1, -1), (-2, -6)]

    # Compute the polygon
    polygon = compute_polygon(points)

    # Plot the points and polygon
    plot_polygon(points, polygon)
