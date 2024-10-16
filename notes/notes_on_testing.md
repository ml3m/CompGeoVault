    /*
	n := flag.Int("n", 50, "Number of random points to generate")
	filename := flag.String("f", "hull", "Output filename prefix for the plot (without extension)")
	benchmark_algorithm := flag.String("alg", "grahamscan", "Selects algorithm (grahamscan or jarvismarch)")
	flag.Parse()

    multipleRunBenchmark(25, *n, *filename, *benchmark_algorithm, )
    */

    //standard run
    // benchmark(*n, *filename, *benchmark_algorithm)

    // testing on geogebra
    // plist = {(0,3),(1,1),(2,2),(4,4),(0,0),(1,2),(3,1),(3,3)}

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
