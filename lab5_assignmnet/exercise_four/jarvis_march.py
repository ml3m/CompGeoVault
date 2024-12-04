import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os

# Ensure the outputs directory exists
os.makedirs('outputs', exist_ok=True)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def orientation(p, q, r):
    """Return the orientation of the triplet (p, q, r).
    0 -> p, q and r are collinear
    1 -> Clockwise
    2 -> Counterclockwise
    """
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def jarvis_march(points):
    """Perform the Jarvis March algorithm on a set of points."""
    n = len(points)
    if n < 3:
        return [], []  # Return empty hull and steps if not enough points

    # Find the leftmost point
    leftmost = 0
    for i in range(1, n):
        if points[i].x < points[leftmost].x:
            leftmost = i
        elif points[i].x == points[leftmost].x:
            if points[i].y > points[leftmost].y:
                leftmost = i

    hull = []
    p = leftmost
    steps = []

    while True:
        hull.append(p)
        q = (p + 1) % n
        steps.append((p, q))  # Store step for animation

        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
                steps.append((p, q))  # Update steps when selecting a new q

        p = q
        if p == leftmost:
            break

    return hull, steps


def plot_hull(step_idx, points, hull, steps):
    ax.clear()

    x_points = [p.x for p in points]
    y_points = [p.y for p in points]

    # Plot all points
    ax.plot(x_points, y_points, 'bo', label='Points')

    # Highlight current step edge
    if steps:
        p, q = steps[step_idx]
        ax.plot([points[p].x, points[q].x], [points[p].y, points[q].y], 'g--', lw=2, label=f'Step {step_idx + 1}')

    # Hull points
    hull_points = [points[idx] for idx in hull[:step_idx + 1]]
    hull_points.append(hull_points[0])  # Close the hull
    hx = [p.x for p in hull_points]
    hy = [p.y for p in hull_points]

    # Plot hull
    ax.plot(hx, hy, 'r-', lw=2, label='Convex Hull')

    ax.set_xlim(-1, 6)
    ax.set_ylim(-2, 4)
    ax.set_title(f'Jarvis March Step {step_idx + 1}')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.legend()
    ax.grid(True)


# Points array
points = [Point(2, -1), Point(1, 3), Point(4, 0), Point(4, 3), Point(5, 2)]

# Run Jarvis March to get the convex hull and steps for animation
hull, steps = jarvis_march(points)

# Create plot and animation
fig, ax = plt.subplots()
animation = FuncAnimation(fig, plot_hull, frames=len(steps), fargs=(points, hull, steps), repeat=False)

# Ensure the steps list is not empty before saving
if steps:
    animation.save('outputs/jarvis_march_animation.gif', writer='pillow', fps=2)

plt.show()
