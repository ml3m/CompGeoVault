package main

import (
    "path/filepath"
	"flag"
    "time"
	"fmt"
    "os"

	"compgeovault/algorithms"
	"compgeovault/geometry"
	"compgeovault/visualizer"

	"gonum.org/v1/plot"
)

func benchmark(n int, filename string, algorithm string) {
    if filepath.Ext(filename) != ".png" { // make sure filename has .png
        filename += ".png"
    }

    if algorithm != "grahamscan" && algorithm != "jarvismarch" && algorithm != "delaunay" {
        fmt.Println("Invalid algorithm specified.")
        algorithms.PrintUsage()
        os.Exit(1)
    }

    var elapsedTime time.Duration
    var points []geometry.Point
    var vertices []algorithms.Vertex

    // time each generation depending on triangulation or convex hull
    startTime := time.Now()
    if algorithm == "delaunay" {
        vertices = algorithms.GenerateRandomVertices(n)
        elapsedTime = time.Since(startTime)
        fmt.Printf("Generated %d random vertices in %s\n", n, elapsedTime)
    } else {
        points = algorithms.GenerateRandomPoints(n)
        elapsedTime = time.Since(startTime)
        fmt.Printf("Generated %d random points in %s\n", n, elapsedTime)
    }

    var hull_list []geometry.Point
    var triangles []algorithms.Triangle
    var alg_print_string string //used for beauty printing

    startTime = time.Now()
    switch algorithm {
        case "grahamscan":
            alg_print_string = "GrahamScan"
            hull_list = algorithms.GrahamScan(points)
        case "jarvismarch":
            alg_print_string = "JarvisMarch"
            hull_list = algorithms.JarvisMarch(points)
        case "delaunay":
            // work in progress
            alg_print_string = "Delaunay Triangulation"
            triangles = algorithms.Delaunay(vertices)
        default:
            fmt.Println("Invalid algorithm. Please choose 'grahamscan' or 'jarvismarch'.")
            return
    }
    elapsedTime = time.Since(startTime)

    // prints triangulation count or hull points count
    if algorithm == "delaunay" {
        fmt.Printf("Using algorithm: %s \nGenerated triangulation in %s with %d triangles\n", alg_print_string, elapsedTime, len(triangles))
    } else {
        fmt.Printf("Using algorithm: %s \nGenerated hull in %s with %d points\n", alg_print_string, elapsedTime, len(hull_list))
    }

    // create plot for each type triangulation/hull
    var p *plot.Plot
    var err error
    if algorithm == "delaunay" {
        p, err = visualizer.CreateDelaunayPlot(vertices, triangles) // Delaunay-specific plot
    } else {
        p, err = visualizer.CreatePlot(points, hull_list) // Convex hull-specific plot
    }
    
    if err != nil { panic(err) }
    if err := visualizer.SavePlot(p, filename); err != nil { panic(err)}

    fmt.Printf("Plot saved as %s\n", filename)
}

/* not used for now */
func multipleRunBenchmark(running_time int, n int, filename string, benchmark_algorithm string){
	for i := 0; i < running_time; i++ {
		fmt.Printf("Executing iteration %d\n", i+1)
		iterFilename := fmt.Sprintf("%s_%d", filename, i+1)
		benchmark(n, iterFilename, benchmark_algorithm)
	}
}

func main(){
    n := flag.Int("n", 50, "Number of random points to generate")
    filename := flag.String("f", "output_plot.png", "Output .png filename for the plot")
    benchmark_algorithm := flag.String("alg", "grahamscan", "Selects algorithm (grahamscan or jarvismarch)")

    flag.Parse()
    benchmark(*n, *filename, *benchmark_algorithm)
}
