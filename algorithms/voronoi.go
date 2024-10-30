/*
 * voronoi.go
 *
 * In this file is implemented the Voronoi Diagram generation based on the Delaunay Triangulation.
 * The Voronoi diagram is calculated by connecting the circumcenters of neighboring triangles.
 *
 * Author: ml3m
 * Date: Oct 18 2024
 */

package algorithms

type VoronoiEdge struct {
    Start Vertex
    End   Vertex
}

type VoronoiCell struct {
    Site  Vertex       // The original point
    Edges []VoronoiEdge // The edges that form the Voronoi cell
}

// Generates the Voronoi diagram from the given Delaunay triangulation
func Voronoi(triangles []Triangle) []VoronoiCell {
    // To store the Voronoi cells
    cells := make(map[Vertex]*VoronoiCell)

    // Iterate over each triangle
    for i, t1 := range triangles {
        circumcenter := t1.CircumCirc.Center

        // Initialize the cell for the current vertex
        addToCell(cells, t1.V0, circumcenter)
        addToCell(cells, t1.V1, circumcenter)
        addToCell(cells, t1.V2, circumcenter)

        // Find the neighbors of the triangle (sharing an edge)
        for j, t2 := range triangles {
            if i != j && isNeighbor(t1, t2) {
                neighborCircumcenter := t2.CircumCirc.Center
                connectCells(cells, t1, circumcenter, neighborCircumcenter)
            }
        }
    }

    // Convert the map to a slice
    var result []VoronoiCell
    for _, cell := range cells {
        result = append(result, *cell)
    }

    return result
}

// Adds a circumcenter to the Voronoi cell of a given vertex
func addToCell(cells map[Vertex]*VoronoiCell, v Vertex, circumcenter Vertex) {
    if _, exists := cells[v]; !exists {
        cells[v] = &VoronoiCell{Site: v, Edges: []VoronoiEdge{}}
    }
    // We will add edges later when we find neighbors
}

// Connects two Voronoi cells by adding an edge between their circumcenters
func connectCells(cells map[Vertex]*VoronoiCell, t Triangle, circumcenter1, circumcenter2 Vertex) {
    for _, v := range []Vertex{t.V0, t.V1, t.V2} {
        if cell, exists := cells[v]; exists {
            cell.Edges = append(cell.Edges, VoronoiEdge{Start: circumcenter1, End: circumcenter2})
        }
    }
}

// Checks if two triangles are neighbors by seeing if they share an edge
func isNeighbor(t1, t2 Triangle) bool {
    sharedVertices := 0
    if t1.V0.Equals(t2.V0) || t1.V0.Equals(t2.V1) || t1.V0.Equals(t2.V2) {
        sharedVertices++
    }
    if t1.V1.Equals(t2.V0) || t1.V1.Equals(t2.V1) || t1.V1.Equals(t2.V2) {
        sharedVertices++
    }
    if t1.V2.Equals(t2.V0) || t1.V2.Equals(t2.V1) || t1.V2.Equals(t2.V2) {
        sharedVertices++
    }
    return sharedVertices == 2
}
