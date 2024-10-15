package visualizer

import (
    "image/color"
    
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"

    "grahamScan/geometry"
)

// CreatePlot initializes and configures the plot
func CreatePlot(points []geometry.Point, hull_list []geometry.Point) (*plot.Plot, error) {
    p := plot.New()

    p.Title.Text = "Points and Convex Hull"
    p.X.Label.Text = "X"
    p.Y.Label.Text = "Y"

    // Pass geometry.Point instead of visualizer.Point
    if err := AddPointsToPlot(p, points); err != nil {
        return nil, err
    }

    // Pass geometry.Point instead of visualizer.Point
    if err := AddHullToPlot(p, hull_list); err != nil {
        return nil, err
    }

    return p, nil
}

// AddPointsToPlot adds points to the plot as a scatter plot
func AddPointsToPlot(p *plot.Plot, points []geometry.Point) error {
    scatterData := make(plotter.XYs, len(points))
    for i, pt := range points {
        scatterData[i].X = pt.X // Use the exported field X
        scatterData[i].Y = pt.Y // Use the exported field Y
    }

    scatter, err := plotter.NewScatter(scatterData)
    if err != nil {
        return err
    }
    scatter.GlyphStyle.Radius = vg.Points(5) // increase point size
    scatter.GlyphStyle.Color = color.RGBA{R: 0, G: 0, B: 255, A: 255} // blue color

    p.Add(scatter)
    return nil
}

// AddHullToPlot adds the convex hull to the plot as a line
func AddHullToPlot(p *plot.Plot, hull_list []geometry.Point) error {
    hullLineData := make(plotter.XYs, len(hull_list)+1)
    for i, pt := range hull_list {
        hullLineData[i].X = pt.X // Use the exported field X
        hullLineData[i].Y = pt.Y // Use the exported field Y
    }
    hullLineData[len(hull_list)] = hullLineData[0]

    hullLine, err := plotter.NewLine(hullLineData)
    if err != nil {
        return err
    }
    hullLine.LineStyle.Width = vg.Points(2)

    p.Add(hullLine)
    return nil
}

// SavePlot saves the plot to a PNG file
func SavePlot(p *plot.Plot, filename string) error {

    // 1536 x 1536 res
    return p.Save(16*vg.Inch, 16*vg.Inch, filename)

}
