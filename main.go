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
    "grahamScan/geometry"
)

func benchmark(n int, filename string, algorithm string) {
    // Check if the filename has a .png extension
    if filepath.Ext(filename) != ".png" {
        filename += ".png"
    }

    // Generate random points
    startTime := time.Now()
    points := algorithms.GenerateRandomPoints(n)
    elapsedTime := time.Since(startTime)
    fmt.Printf("Generated %d random points in %s\n", n, elapsedTime)

    // Determine the algorithm to use
    var hull_list []geometry.Point
    var alg_print_string string //used for beauty printing

    startTime = time.Now()
    switch algorithm {
    case "grahamscan":
        alg_print_string = "GrahamScan"
        hull_list = algorithms.GrahamScan(points)
    case "jarvismarch":
        alg_print_string = "JarvisMarch"
        hull_list = algorithms.JarvisMarch(points)
    default:
        fmt.Println("Invalid algorithm. Please choose 'grahamscan' or 'jarvismarch'.")
        return
    }
    elapsedTime = time.Since(startTime)
    fmt.Printf("Using algorithm: %s \nGenerated hull in %s with %d points\n", alg_print_string, elapsedTime, len(hull_list))

    // Create and save the plot
    p, err := visualizer.CreatePlot(points, hull_list)
    if err != nil {
        panic(err)
    }

    if err := visualizer.SavePlot(p, filename); err != nil {
        panic(err)
    }

    fmt.Printf("Plot saved as %s\n", filename)
}

func main(){

    n := flag.Int("n", 50, "Number of random points to generate")
    filename := flag.String("f", "hull.png", "Output .png filename for the plot")
    benchmark_algorithm := flag.String("alg", "grahamscan", "Selects algorithm (grahamscan or jarvismarch)")
    flag.Parse()

    benchmark(*n, *filename, *benchmark_algorithm)


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
