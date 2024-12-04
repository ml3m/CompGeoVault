package algorithms

import (
	"compgeovault/geometry"
)

func JarvisMarch(points []geometry.Point) []geometry.Point {
    // exit case
	if len(points) < 3 {
		return points 
	}

	var hull_list []geometry.Point
	y_leftmost := 0

	// find the leftmost point
	for i := 1; i < len(points); i++ {
		if points[i].X < points[y_leftmost].X {
			y_leftmost = i
		}
	}

	p := y_leftmost

	for {
		hull_list = append(hull_list, points[p])
		q := (p + 1) % len(points) // next point in the list

		// find the most counter-clockwise point relative to point p
		for i := 0; i < len(points); i++ {
			if orientation(points[p], points[i], points[q]) > 0 {
				q = i
			}
		}

		p = q // move to the next point
		if p == y_leftmost { // we wrapped around to the starting point
			break
		}
	}
	return hull_list
}
