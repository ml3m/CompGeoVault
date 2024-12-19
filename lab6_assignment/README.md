# Lab 6 Assignment: Voronoi Diagrams, Delaunay Triangulation, and More

This repository contains solutions and implementations for computational geometry problems related to Voronoi diagrams, Delaunay triangulations, and minimal spanning trees. Each exercise is organized into separate directories with relevant code and supporting images.

---

## Table of Contents
1. [How to Use](#how-to-use)
2. [Exercises](#exercises)
   - [Exercise 1](#exercise-1)
   - [Exercise 2](#exercise-2)
   - [Exercise 3](#exercise-3)
   - [Exercise 4](#exercise-4)
   - [Exercise 5](#exercise-5)
   - [Exercise 6](#exercise-6)
3. [Requirements](#requirements)

---

## How to Use

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd lab6_assignment
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the implementations for each exercise:
   ```bash
   python <path-to-implementation.py>
   ```

   Replace `<path-to-implementation.py>` with the path to the relevant script.

---

## Exercises

### Exercise 1
**Problem**: Determine the Voronoi diagram and Delaunay triangulation for the points:  
A = (3, 5), B = (6, 6), C = (6, 4), D = (9, 5), and E = (9, 7).  

**Files**:
- [Code: `exercise_one/implement.py`](./exercise_one/implement.py)
- [Voronoi Functionality: `exercise_one/voronoi.py`](./exercise_one/voronoi.py)
- [Visualization: `exercise_one/3graphs_exercise_1.png`](./exercise_one/3graphs_exercise_1.png)

---

### Exercise 2
**Problem**: Find a set of two points {A7, A8} such that the Voronoi diagram of {A1, ..., A8} has exactly 4 half-line edges.  

**Files**:
- [Code: `exercise_two/implementation.py`](./exercise_two/implementation.py)
- [Explanation: `exercise_two/ex_2.png`](./exercise_two/ex_2.png)

---

### Exercise 3
**Problem**: Determine the value of λ for which the minimal spanning tree of given points has the smallest length.  

**Files**:
- [Code: `exercise_three/minimum_spanning_tree_lambda.py`](./exercise_three/minimum_spanning_tree_lambda.py)
- [Explanation: `exercise_three/ex3_2.png`](./exercise_three/ex3_2.png)

---

### Exercise 4
**Problem**: Find the number of half-lines in the Voronoi diagram for the given set of points.  

**Files**:
- [Code: `exercise_four/implementation.py`](./exercise_four/implementation.py)
- [Visualization: `exercise_four/ex4.png`](./exercise_four/ex4.png)

---

### Exercise 5
**Problem**: Provide two sets of points with different sizes that result in triangulations with exactly 5 triangle faces.  

**Files**:
- [Code: `exercise_five/implementation.py`](./exercise_five/implementation.py)
- [Visualization: `exercise_five/ex5.png`](./exercise_five/ex5.png)

---

### Exercise 6
**Problem**: Write an algorithm to calculate the number of triangles and edges in the triangulation for a parameterized set of points.  

**Files**:
- [Code: `exercise_six/implementation.py`](./exercise_six/implementation.py)
- [Visualization: `exercise_six/ex6.png`](./exercise_six/ex6.png)

---

## Additional Resources

- **Fortune's Sweep Line Implementation**:
  - [Code: `fortunes_sweep_line_voronoi/fortunes_sweeping_line.py`](./fortunes_sweep_line_voronoi/fortunes_sweeping_line.py)
  - [Demo Video: `fortunes_sweep_line_voronoi/Screen Recording 2024-12-19 at 22.19.54.mov`](./fortunes_sweep_line_voronoi/Screen%20Recording%202024-12-19%20at%2022.19.54.mov)

- **References and Links**:  
  - [Geogebra Links: `geogebra_links.txt`](./geogebra_links.txt)

---

## Requirements

Ensure you have Python installed, along with the required libraries. The dependencies are listed in the `requirements.txt` file.

Install them with:
```bash
pip install -r requirements.txt
```
