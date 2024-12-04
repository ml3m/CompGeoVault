package main

import (
    "flag"
    "fmt"
    "os"
    "path/filepath"
    "time"

    "compgeovault/algorithms"
    "compgeovault/geometry"
    "compgeovault/visualizer"

    "gonum.org/v1/plot"
)

func DEBUG_PrintPoints(points []geometry.Point) {
    fmt.Println("Points:")
    for i, point := range points {
        fmt.Printf("Point %d: (%.2f, %.2f)\n", i, point.X, point.Y)
    }
}

func benchmark(n int, filename string, algorithm string) {
    if filepath.Ext(filename) != ".png" { // make sure filename has .png
        filename += ".png"
    }

    // Validate algorithm input
    if algorithm != "grahamscan" && algorithm != "jarvismarch" && algorithm != "delaunay" && algorithm != "voronoi" {
        fmt.Println("Invalid algorithm specified.")
        algorithms.PrintUsage()
        os.Exit(1)
    }

    var elapsedTime time.Duration
    var points []geometry.Point
    var vertices []algorithms.Vertex

    // Time the point/vertex generation based on algorithm type
    startTime := time.Now()
    if algorithm == "delaunay" || algorithm == "voronoi" {
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
    var voronoiCells []algorithms.VoronoiCell
    var alg_print_string string // used for printing details

    // Choose the algorithm and execute it
    startTime = time.Now()
    switch algorithm {
    case "grahamscan":
        alg_print_string = "GrahamScan"
        hull_list = algorithms.GrahamScan(points)

    case "jarvismarch":
        alg_print_string = "JarvisMarch"
        hull_list = algorithms.JarvisMarch(points)
    case "delaunay":
        alg_print_string = "Delaunay Triangulation"
        triangles = algorithms.Delaunay(vertices)
    case "voronoi":
        alg_print_string = "Voronoi Diagram"
        triangles = algorithms.Delaunay(vertices) // Delaunay Triangulation is required for Voronoi diagram
        voronoiCells = algorithms.Voronoi(triangles)
    default:
        fmt.Println("Invalid algorithm. Please choose 'grahamscan', 'jarvismarch', 'delaunay', or 'voronoi'.")
        return
    }
    elapsedTime = time.Since(startTime)

    // Print triangulation or hull points count based on algorithm
    switch algorithm {
    case "delaunay":
        fmt.Printf("Using algorithm: %s \nGenerated triangulation in %s with %d triangles\n", alg_print_string, elapsedTime, len(triangles))
    case "voronoi":
        fmt.Printf("Using algorithm: %s \nGenerated Voronoi diagram in %s with %d cells\n", alg_print_string, elapsedTime, len(voronoiCells))
    default:
        fmt.Printf("Using algorithm: %s \nGenerated hull in %s with %d points\n", alg_print_string, elapsedTime, len(hull_list))
    }

    // Create plot based on algorithm type
    var p *plot.Plot
    var err error
    switch algorithm {
    case "delaunay":
        p, err = visualizer.CreateDelaunayPlot(vertices, triangles)
    case "voronoi":
        p, err = visualizer.CreateVoronoiPlot(vertices, voronoiCells)
    default:
        p, err = visualizer.CreatePlot(points, hull_list)
    }

    if err != nil {
        panic(err)
    }
    if err := visualizer.SavePlot(p, filename); err != nil {
        panic(err)
    }

    fmt.Printf("Plot saved as %s\n", filename)
}

/* Not used for now */
func multipleRunBenchmark(running_time int, n int, filename string, benchmark_algorithm string) {
    for i := 0; i < running_time; i++ {
        fmt.Printf("Executing iteration %d\n", i+1)
        iterFilename := fmt.Sprintf("%s_%d", filename, i+1)
        benchmark(n, iterFilename, benchmark_algorithm)
    }
}

func main() {
    n := flag.Int("n", 50, "Number of random points to generate")
    filename := flag.String("f", "output_plot.png", "Output .png filename for the plot")
    benchmark_algorithm := flag.String("alg", "grahamscan", "Selects algorithm (grahamscan, jarvismarch, delaunay, voronoi)")

    flag.Parse()
    benchmark(*n, *filename, *benchmark_algorithm)
}
