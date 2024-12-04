/*
 * delaunay.go
 *
 * in this file is implemented the Delaunay Triangulation algorithm using the
 * Bowyer-Watson method. The algorithm is based on the pseudocode and 
 * indications given in the following resources:
 *
 * -  Bowyer-Watson Algorithm for Delaunay Triangulation (pseudocode guide)- 
 *    https://www.gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation
 *
 * The implementation follows the guidelines and logic presented in these 
 * references to achieve accurate and efficient triangulation of points.
 *
 * Author: ml3m
 * Date: Oct 16 2024
 */

package algorithms

import (
    "math"
)

type Vertex struct {
    X float64
    Y float64
}
type Edge struct {
    V0 Vertex
    V1 Vertex
}
type Circle struct { // used for representing the circumcircle of a triangle
    Center Vertex
    Radius float64
}
type Triangle struct {
    V0, V1, V2 Vertex
    CircumCirc Circle
}


// checks if two vertices are equal
func (v Vertex) Equals(other Vertex) bool {
    return v.X == other.X && v.Y == other.Y
}

// checks if two edges are equal (ignoring direction)
func (e Edge) Equals(other Edge) bool {
    return (e.V0.Equals(other.V0) && e.V1.Equals(other.V1)) ||
        (e.V0.Equals(other.V1) && e.V1.Equals(other.V0))
}

// creates a new Triangle and calculates its circumcircle, since Triangle has
// field: CircumCirc type Circle it is placed there.
func NewTriangle(v0, v1, v2 Vertex) Triangle {
    return Triangle{
        V0:         v0,
        V1:         v1,
        V2:         v2,
        CircumCirc: calcCircumCircle(v0, v1, v2),
    }
}

// checks if a given vertex is inside the circumcircle of the triangle
func (t Triangle) InCircumcircle(v Vertex) bool {
    dx := t.CircumCirc.Center.X - v.X
    dy := t.CircumCirc.Center.Y - v.Y
    distance := math.Sqrt(dx*dx + dy*dy)
    return distance <= t.CircumCirc.Radius
}

// calculates the circumcircle for a given triangle
func calcCircumCircle(v0, v1, v2 Vertex) Circle {
    dA := v0.X*v0.X + v0.Y*v0.Y
    dB := v1.X*v1.X + v1.Y*v1.Y
    dC := v2.X*v2.X + v2.Y*v2.Y

    aux1 := (dA * (v2.Y - v1.Y)) + (dB * (v0.Y - v2.Y)) + (dC * (v1.Y - v0.Y))
    aux2 := -(dA * (v2.X - v1.X)) - (dB * (v0.X - v2.X)) - (dC * (v1.X - v0.X))
    div := 2 * (v0.X*(v2.Y-v1.Y) + v1.X*(v0.Y-v2.Y) + v2.X*(v1.Y-v0.Y))

    centerX := aux1 / div
    centerY := aux2 / div
    center := Vertex{centerX, centerY}

    dx := center.X - v0.X
    dy := center.Y - v0.Y
    radius := math.Sqrt(dx*dx + dy*dy)

    return Circle{Center: center, Radius: radius}
}

// core
// triangulate generates a Delaunay triangulation from a list of vertices.
func Delaunay(vertices []Vertex) []Triangle {
    // Create bounding 'super' triangle
    st := makeSuperTriangle(vertices)

    // Initialize triangles with the super triangle
    triangles := []Triangle{st}

    // Triangulate each vertex
    for _, vertex := range vertices {
        triangles = addVertex(vertex, triangles)
    }

    // Remove triangles that share edges with the super triangle
    var finalTriangles []Triangle
    for _, triangle := range triangles {
        if !(triangle.V0.Equals(st.V0) || triangle.V0.Equals(st.V1) || triangle.V0.Equals(st.V2) ||
            triangle.V1.Equals(st.V0) || triangle.V1.Equals(st.V1) || triangle.V1.Equals(st.V2) ||
            triangle.V2.Equals(st.V0) || triangle.V2.Equals(st.V1) || triangle.V2.Equals(st.V2)) {
            finalTriangles = append(finalTriangles, triangle)
        }
    }

    return finalTriangles
}

// addVertex updates the array of triangles by adding a new vertex.
func addVertex(vertex Vertex, triangles []Triangle) []Triangle {
    var edges []Edge

    // remove triangles with circumcircles containing the vertex
    var updatedTriangles []Triangle
    for _, triangle := range triangles {
        if triangle.InCircumcircle(vertex) {
            edges = append(edges, Edge{triangle.V0, triangle.V1})
            edges = append(edges, Edge{triangle.V1, triangle.V2})
            edges = append(edges, Edge{triangle.V2, triangle.V0})
        } else {
            updatedTriangles = append(updatedTriangles, triangle)
        }
    }

    uniqueEdges := getUniqueEdges(edges) // get unique edges

    // create new triangles from the unique edges and new vertex
    for _, edge := range uniqueEdges {
        updatedTriangles = append(updatedTriangles, NewTriangle(edge.V0, edge.V1, vertex))
    }
    return updatedTriangles
}

// removes duplicate edges.
func getUniqueEdges(edges []Edge) []Edge {
    var uniqueEdges []Edge

    for i := 0; i < len(edges); i++ {
        isUnique := true

        for j := 0; j < len(edges); j++ {
            if i != j && edges[i].Equals(edges[j]) {
                isUnique = false
                break
            }
        }

        if isUnique {
            uniqueEdges = append(uniqueEdges, edges[i])
        }
    }

    return uniqueEdges
}

//creates a super triangle that contain all vertices.
func makeSuperTriangle(vertices []Vertex) Triangle {
    // the technique of bounding box of all the vertices
    minX, minY := math.MaxFloat64, math.MaxFloat64
    maxX, maxY := -math.MaxFloat64, -math.MaxFloat64

    for _, v := range vertices {
        if v.X < minX {
            minX = v.X
        }
        if v.X > maxX {
            maxX = v.X
        }
        if v.Y < minY {
            minY = v.Y
        }
        if v.Y > maxY {
            maxY = v.Y
        }
    }

    // expanding the BD just a bit for safety... (not really studied this one)
    // can be refined, it shouldn't impact performance/result a lot
    dx := maxX - minX
    dy := maxY - minY
    deltaMax := math.Max(dx, dy) * 10

    v0 := Vertex{minX - deltaMax, minY - deltaMax}
    v1 := Vertex{minX + 2*deltaMax, minY - deltaMax}
    v2 := Vertex{minX, minY + 2*deltaMax}

    return NewTriangle(v0, v1, v2)
}
