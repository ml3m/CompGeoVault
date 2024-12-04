# Andrew's Convex Hull Algorithm Visualization

## Problem Description
Determine the lower edge of the convex hull for a set of points M = {P1, P2, ..., P7}, where:
- P1 = (1, 10)
- P2 = (-2, 7)
- P3 = (3, 8)
- P4 = (4, 10)
- P5 = (5, 7)
- P6 = (6, 7)
- P7 = (7, 11)

## Algorithm
This implementation uses Andrew's variant of Graham's scan to find the lower convex hull, which:
- Sorts points lexicographically
- Builds the hull by iteratively adding points
- Removes points that create non-left turns
- Tracks the evolution of hull vertices

## Visualization Lower Convex Hull Formation after Andrew's Graham's Scan Variant
![Lower Convex Hull Formation Animation](./lower_hull_animation.gif)

Visualization shows:
- Blue points: Original point set
- Red point: Current point being processed
- Green line: Lower hull
- Light pink area: Region above the lower hull path

## Methodology
1. Sort input points
2. Iterate through points
3. Check point orientations
4. Build lower hull incrementally
5. Animate hull formation steps

## Visualization Detail
- Tracks each step of hull formation
- Shows point addition/removal process
- Highlights current point being evaluated
- Colors area above lower hull

## Output
- Animated matplotlib visualization
- GIF of convex hull formation
