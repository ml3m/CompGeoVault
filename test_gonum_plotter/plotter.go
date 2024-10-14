package main

import (
    "math/rand"

    "gonum.org/v1/plot"
    "gonum.org/v1/plot/plotter"
    "gonum.org/v1/plot/vg"
)

func main() {
    // Generate random points
    nPoints := 10
    points := make(plotter.XYs, nPoints)
    for i := range points {
        points[i].X = rand.Float64() * 10 // Generate random X between 0 and 10
        points[i].Y = rand.Float64() * 10 // Generate random Y between 0 and 10
    }

    // Calculate convex hull (implement your Graham scan here)
    hull := calculateConvexHull(points)

    // Create a new plot
    p:= plot.New()

    // Set title and labels
    p.Title.Text = "Points and Convex Hull"
    p.X.Label.Text = "X"
    p.Y.Label.Text = "Y"

    // Create a scatter plot for points
    scatter, err := plotter.NewScatter(points)
    if err != nil {
        panic(err)
    }
    scatter.GlyphStyle.Radius = vg.Points(3)

    // Add scatter points to the plot
    p.Add(scatter)

    // Create a line plot for the hull
    hullLine, err := plotter.NewLine(hull)
    if err != nil {
        panic(err)
    }
    hullLine.LineStyle.Width = vg.Points(1)
    hullLine.LineStyle.Color = plotter.DefaultLineStyle.Color // Set a different color for the hull

    // Add the hull line to the plot
    p.Add(hullLine)

    // Save the plot to a PNG file
    if err := p.Save(4*vg.Inch, 4*vg.Inch, "hull.png"); err != nil {
        panic(err)
    }
}

// Dummy function for calculating the convex hull
// Replace this with your actual Graham scan implementation
func calculateConvexHull(points plotter.XYs) plotter.XYs {
    hull := make(plotter.XYs, 0)
    // Example: Add the first and last points to the hull (replace with actual points)
    if len(points) > 1 {
        hull = append(hull, points[0], points[1], points[0]) // Closing the hull by returning to the first point
    }
    return hull
}
