// testing on geogebra
// plist = {(0,3),(1,1),(2,2),(4,4),(0,0),(1,2),(3,1),(3,3)}
package main

import (
	"flag"
	"fmt"
	"time"
    "path/filepath"

	"grahamScan/algorithms"
	"grahamScan/visualizer"
)

func benchmark1(n int, filename string) {

    if filepath.Ext(filename) != ".png" {
        filename += ".png"
    }

    startTime := time.Now()
    points := algorithms.GenerateRandomPoints(n)
    elapsedTime := time.Since(startTime)
    fmt.Printf("Generated %d random points in %s\n", n, elapsedTime)

    startTime = time.Now()
    hull_list := algorithms.GrahamScan(points)
    elapsedTime = time.Since(startTime)
    fmt.Printf("Using GrahamScan Algorithm\nGenerated hull in %s with %d points\n", elapsedTime, len(hull_list))

    p, err := visualizer.CreatePlot(points, hull_list)
    if err != nil {
        panic(err)
    }

    if err := visualizer.SavePlot(p, filename); err != nil {
        panic(err)
    }

    fmt.Printf("Plot saved as: %s", filename)
}

func benchmark2(n int, filename string) {

    if filepath.Ext(filename) != ".png" {
        filename += ".png"
    }

    startTime := time.Now()
    points := algorithms.GenerateRandomPoints(n)
    elapsedTime := time.Since(startTime)
    fmt.Printf("Generated %d random points in %s\n", n, elapsedTime)

    startTime = time.Now()
    hull_list := algorithms.JarvisMarch(points)
    elapsedTime = time.Since(startTime)
    fmt.Printf("Using JarvisMarch Algorithm\nGenerated hull in %s with %d points\n", elapsedTime, len(hull_list))


    p, err := visualizer.CreatePlot(points, hull_list)
    if err != nil {
        panic(err)
    }

    if err := visualizer.SavePlot(p, filename); err != nil {
        panic(err)
    }

    fmt.Printf("Plot saved as: %s", filename)
}

func main(){

    n := flag.Int("n", 50, "Number of random points to generate")
    filename := flag.String("f", "hull.png", "Output .png filename for the plot")
    benchmark := flag.String("alg", "grahamscan", "Selects algorithm (grahamscan or jarvismarch)")
    flag.Parse()

    switch *benchmark {
    case "grahamscan":
        benchmark1(*n, *filename)
    case "jarvismarch":
        benchmark2(*n, *filename)
    default:
        fmt.Println("Invalid algorithm. Please choose 'grahamscan' or 'jarvismarch'.")
    }

    /*
	// Testing points (you can comment this out and use random points instead)
	points := []Point{{0, 3}, {1, 1}, {2, 2}, {4, 4}, {0, 0}, {1, 2}, {3, 1}, {3, 3}}

	// Generate random points if needed
	// n := 100 // Number of points
	// points := GenerateRandomPoints(n)

	hull_list := grahamScan(points)

	// Create and save the plot
	p, err := createPlot(points, hull_list)
	if err != nil {
		panic(err)
	}

	if err := savePlot(p, "hull.png"); err != nil {
		panic(err)
	}

	fmt.Println("Plot saved as hull.png")
    */


    /*
    // for some testing  (geogebra)
    points := []Point{{0, 3}, {1, 1}, {2, 2}, {4, 4},
                      {0, 0}, {1, 2}, {3, 1}, {3, 3}};
    */

    // some tests
    /*
        ➜  GrahamScan git:(main) ✗ go run grahamScan.go
        Generated 10000000 random points in 330.75ms
        Generated hull in 10.916514417s with 43 points

        Generated 100000000 random points in 4.033935417s
        Generated hull in 2m36.6532265s with 48 points
    */

    // testing benchmark
    /*
    n := 100000000
    
    startTime := time.Now()
    points := GenerateRandomPoints(n)
    elapsedTime := time.Since(startTime) 

    fmt.Printf("Generated %d random points in %s\n", n, elapsedTime)

    startTime = time.Now()
    hull_list := grahamScan(points)
    elapsedTime = time.Since(startTime) 

    fmt.Printf("Generated hull in %s with %d points\n", elapsedTime, len(hull_list))

    //fmt.Println(hull_list)
    */
}
