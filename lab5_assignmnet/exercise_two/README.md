# Convex Hull Border Points Algorithm

This Python project calculates and visualizes the points that lie on the border of the convex hull of a set of points, including a user-defined point \( M \) that depends on the parameter \( \lambda \).

## Problem Description

Given the fixed points:

- \( A = (3, -3) \)
- \( B = (3, 3) \)
- \( C = (-3, -3) \)
- \( D = (-3, 3) \)

And a moving point \( M = (-2 + \lambda, 3 - \lambda) \), where \( \lambda \in \mathbb{R} \), the task is to:

1. Compute the convex hull of the set of points \( A \), \( B \), \( C \), \( D \), and \( M \).
2. Determine how many of the points lie on the border of the convex hull for different values of \( \lambda \).
3. Visualize the points, the convex hull, and the points on the border using `matplotlib`.

## Features

- **Convex Hull Computation**: Uses the QuickHull algorithm to compute the convex hull.
- **Border Detection**: Identifies how many of the points lie on the border of the convex hull for each value of \( \lambda \).
- **Visualization**: Plots the points, the convex hull, and highlights the border points using `matplotlib`.

## Requirements

- Python 3.x
- Libraries:
  - `numpy`
  - `matplotlib`
  - `convexhull_quickhull_implementation` (for the QuickHull algorithm)

You can install the required libraries using the following command:

```bash
pip install numpy matplotlib
```

Make sure you have the `ConvexHull_QuickHull` implementation in the project for the convex hull computation.

## Usage

### 1. Define Points

The fixed points \( A \), \( B \), \( C \), and \( D \) are predefined in the code. The point \( M \) is dynamically computed based on the given value of \( \lambda \).

### 2. Test with Various \( \lambda \) Values

You can test how many points lie on the convex hull border for different values of \( \lambda \) by modifying the list `lambda_values` in the script.

For example:

```python
lambda_values = [0, 1, -1, 2, -2]
```

### 3. Visualize Results

The script will plot the points, the convex hull, and the points on the border for each \( \lambda \). It will also print how many points are on the border for each value of \( \lambda \).

### Example Output:

```
For λ = 0, 3 points are on the convex hull.
For λ = 1, 3 points are on the convex hull.
For λ = -1, 3 points are on the convex hull.
For λ = 2, 4 points are on the convex hull.
For λ = -2, 4 points are on the convex hull.
```

### 4. View the Plot

For each \( \lambda \), a plot will be shown with:

- Blue circles representing all points.
- Black lines representing the convex hull.
- Red circles representing the vertices of the convex hull.
- Labels for the points \( A \), \( B \), \( C \), \( D \), and \( M \).
