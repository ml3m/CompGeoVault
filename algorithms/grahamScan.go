package algorithms

import(
	"math"
	"math/rand"
    "time"
	"sort"
    "grahamScan/geometry"
)


// polar angle of two points
func polarAngle(a, b geometry.Point) float64 {
    // θ = arctan(y/x). 
    return math.Atan2(b.Y - a.Y, b.X - a.X)
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

func orientation(A, B, C geometry.Point) float64{
    // this is the det of the matrix
    return (B.X*C.Y + A.X*B.Y + A.Y*C.X) - (A.Y*B.X + B.Y*C.X + A.X*C.Y)
}

func GrahamScan(points []geometry.Point) []geometry.Point {

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

func GenerateRandomPoints(n int) []geometry.Point {
    rand.Seed(time.Now().UnixNano()) // Seed the random number generator.
    points := make([]geometry.Point, n)

    for i := 0; i < n; i++ {
        points[i] = geometry.Point{
            X: rand.Float64()*200 - 10000, // Generate a random float between -100 and 100 for X.
            Y: rand.Float64()*200 - 10000, // Generate a random float between -100 and 100 for Y.
        }
    }

    return points
}
