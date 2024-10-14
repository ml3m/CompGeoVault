package algorithms

import (
	"fmt"
	"grahamScan/geometry"
	"sort"
)

func GrahamScan(points []geometry.Point) []geometry.Point {
    if len(points) < 3{
        fmt.Print("a hull with less than 3 points is not that possible\n")
        return points
    }

    // find y lowest point.
    sort.Slice(points, func(i, j int) bool{
        if points[i].Y == points[j].Y {
            return points[i].X < points[j].X
        }
        return points[i].Y < points[j].Y
    })

    y_lowest := points[0]

    // sort all points in CCW order 
    sort.Slice(points[1:], func(i, j int) bool {
        return polarAngle(y_lowest, points[i+1]) < polarAngle(y_lowest, points[j+1])
    })

    // starting line made of first point: y_lowest and the one that forms the
    // lower polar angle.
    hull_list := []geometry.Point{y_lowest, points[1]}

    // iterate trough each point.
    for i := 2; i < len(points); i++ {
        // checks whether adding the current point would maintain "left turn"
        // that is relative to the two points in [] hull_list.

        // have to check for orientation of 2 points that are in hull_list and
        // the one we check for.
        for len(hull_list) > 1 && orientation(
                                    hull_list[len(hull_list) - 2], 
                                    hull_list[len(hull_list) - 1],
                                    points[i])  <= 0 {
            hull_list = hull_list[:len(hull_list) -1]
        }
        hull_list = append(hull_list, points[i])
    }
    return hull_list
}
