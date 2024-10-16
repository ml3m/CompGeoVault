package visualizer

import (
	"image/color"

	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"

	"grahamScan/algorithms"
	"grahamScan/geometry"
)

// creates a plot for the Delaunay triangulation, it may be used for other algorithms in the future.
func CreateDelaunayPlot(points []algorithms.Vertex, triangles []algorithms.Triangle) (*plot.Plot, error) {
    p := plot.New() // Create a new plot
    p.Title.Text = "Delaunay Triangulation"
    p.X.Label.Text = "X"
    p.Y.Label.Text = "Y"

    // add vertices and triangles to the plot
    // plot is returned nil if there is an error.
    if err := addPointsToPlot(p, points, color.RGBA{R: 0, G: 0, B: 255, A: 255}); err != nil { return nil, err }
    if err := addTrianglesToPlot(p, triangles); err != nil { return nil, err }

    return p, nil
}

/*
adds points to the plot as a scatter plot.
adds Triangles to the plot also  both two functions
returns an error or nil */
func addPointsToPlot(p *plot.Plot, points []algorithms.Vertex, pointColor color.RGBA) error {
    scatterData := make(plotter.XYs, len(points))
    for i, pt := range points {
        scatterData[i].X = pt.X
        scatterData[i].Y = pt.Y
    }

    scatter, err := plotter.NewScatter(scatterData)
    if err != nil { return err }
    scatter.GlyphStyle.Radius = vg.Points(5)
    scatter.GlyphStyle.Color = pointColor

    p.Add(scatter)
    return nil
}
func addTrianglesToPlot(p *plot.Plot, triangles []algorithms.Triangle) error {
    for _, tri := range triangles {
        triangleLineData := plotter.XYs{
            {X: tri.V0.X, Y: tri.V0.Y}, // V0 is A
            {X: tri.V1.X, Y: tri.V1.Y}, // V1 is B
            {X: tri.V2.X, Y: tri.V2.Y}, // V2 is C
            {X: tri.V0.X, Y: tri.V0.Y}, // close Triangle
        }

        line, err := plotter.NewLine(triangleLineData)

        if err != nil { return err }

        line.LineStyle.Width = vg.Points(1)
        line.LineStyle.Color = color.RGBA{R: 255, G: 0, B: 0, A: 255} // triangles lines color

        p.Add(line)
    }
    return nil
}

// initializes and configures the plot
func CreatePlot(points []geometry.Point, hull_list []geometry.Point) (*plot.Plot, error) {
    p := plot.New()

    p.Title.Text = "Main Plot"
    p.X.Label.Text = "X"
    p.Y.Label.Text = "Y"

    // pass geometry.Point
    if err := AddPointsToPlot(p, points); err != nil { return nil, err }
    if err := AddHullToPlot(p, hull_list); err != nil { return nil, err }

    return p, nil
}

// adds points to the plot as a scatter plot
func AddPointsToPlot(p *plot.Plot, points []geometry.Point) error {
    scatterData := make(plotter.XYs, len(points))
    for i, pt := range points {
        scatterData[i].X = pt.X // Use the exported field X
        scatterData[i].Y = pt.Y // Use the exported field Y
    }

    scatter, err := plotter.NewScatter(scatterData)

    if err != nil { return err }

    scatter.GlyphStyle.Radius = vg.Points(5) // increase point size
    scatter.GlyphStyle.Color = color.RGBA{R: 0, G: 0, B: 255, A: 255} // line color

    p.Add(scatter)
    return nil
}


// adds the convex hull to the plot as a line
func AddHullToPlot(p *plot.Plot, hull_list []geometry.Point) error {
    hullLineData := make(plotter.XYs, len(hull_list)+1)
    for i, pt := range hull_list {
        hullLineData[i].X = pt.X // Use the exported field X
        hullLineData[i].Y = pt.Y // Use the exported field Y
    }

    hullLineData[len(hull_list)] = hullLineData[0]
    hullLine, err := plotter.NewLine(hullLineData)

    if err != nil { return err }

    hullLine.LineStyle.Width = vg.Points(2)

    p.Add(hullLine)
    return nil
}

// saves the plot to a PNG file
// 1536 x 1536 res
func SavePlot(p *plot.Plot, filename string) error {
    return p.Save(16*vg.Inch, 16*vg.Inch, filename)

    // for higher resolution
    //return p.Save(30*vg.Inch, 30*vg.Inch, filename)
}
