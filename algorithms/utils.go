package algorithms

import (
	"grahamScan/geometry"
	"math"
	"math/rand"
	"time"
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

func GenerateRandomPoints(n int) []geometry.Point {
    // deprecated but don't need to change it for now.
    // rand.Seed() doesn't need to take seed anymore. has its own.
    rand.Seed(time.Now().UnixNano()) 
            
    points := make([]geometry.Point, n)

    for i := 0; i < n; i++ {
        points[i] = geometry.Point{

         // generate a random float between -10000 and 10000 for X and Y.
 
            X: rand.Float64()*20000 - 10000,
            Y: rand.Float64()*20000 - 10000, 
        }
    }
    return points
}
