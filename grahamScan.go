// testing on geogebra
//plist = {(0,3),(1,1),(2,2),(4,4),(0,0),(1,2),(3,1),(3,3)}
//
package main

import (
	"fmt"
	"math"
	"sort"
)

type Point struct{
    x, y float64
}

// polar angle of two points
func polarAngle(a, b Point) float64 {
    // θ = arctan(y/x). 
    return math.Atan2(b.y - a.y, b.x - a.x)
}

/*
 Orientation of a simple polygon 
 https://en.wikipedia.org/wiki/Curve_orientation#Orientation_of_a_simple_polygon
 find det() of this:
 x1 y1 1
 x2 y2 1
 x3 y3 1

 ** det < 0 -> polygon is oriented CW
 ** det > 0 -> polygon is oriented CCW

*/

func orientation(A, B, C Point) float64{
    // this is the det of the matrix
    return (B.x*C.y + A.x*B.y + A.y*C.x) - (A.y*B.x + B.y*C.x + A.x*C.y)
}


func grahamScan(points []Point) []Point {

    // find y lowest point.
    sort.Slice(points, func(i, j int) bool{
        if points[i].y == points[j].y {
            return points[i].x < points[j].x
        }
        return points[i].y < points[j].y
    })

    y_lowest := points[0]

    // sort all points in CCW order 
    sort.Slice(points[1:], func(i, j int) bool {
        return polarAngle(y_lowest, points[i+1]) < polarAngle(y_lowest, points[j+1])
    })

    // starting line made of first point: y_lowest and the one that forms the
    // lower polar angle.
    hull_list := []Point{y_lowest, points[1]}

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

func main(){
    points := []Point{{0, 3}, {1, 1}, {2, 2}, {4, 4},
                      {0, 0}, {1, 2}, {3, 1}, {3, 3}};
    hull_list := grahamScan(points)
    fmt.Println(hull_list)
}


