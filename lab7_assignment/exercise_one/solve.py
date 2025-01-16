import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation, PillowWriter
from typing import List, Tuple

class ArtGalleryProblem:
    def __init__(self, polygon_vertices: List[Tuple[float, float]], vertex_names=None):
        self.vertices = np.array(polygon_vertices)
        self.triangulation = []
        self.colors = {}
        self.guards = []
        
        # Generate vertex names if not provided
        if vertex_names is None:
            self.vertex_names = [f'P{i}' for i in range(len(polygon_vertices))]
        else:
            self.vertex_names = vertex_names
        
        # Setup the plot
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.ax.set_xlim(min(v[0] for v in polygon_vertices) - 20, 
                        max(v[0] for v in polygon_vertices) + 20)
        self.ax.set_ylim(min(v[1] for v in polygon_vertices) - 20, 
                        max(v[1] for v in polygon_vertices) + 20)
    
    def compute_angle(self, p1, p2, p3):
        """Compute angle between three points."""
        v1 = np.array(p1) - np.array(p2)
        v2 = np.array(p3) - np.array(p2)
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        return np.degrees(angle)

    def is_ear(self, vertices, i):
        """Check if vertex i forms an ear with its neighbors."""
        n = len(vertices)
        prev = vertices[(i-1) % n]
        curr = vertices[i]
        next_vertex = vertices[(i+1) % n]
        
        # Check if the angle is less than 180 degrees
        angle = self.compute_angle(prev, curr, next_vertex)
        if angle >= 180:
            return False
        
        # Create triangle from the three points
        triangle = [prev, curr, next_vertex]
        
        # Check if any other vertex is inside this triangle
        for j, vertex in enumerate(vertices):
            if vertex in triangle:
                continue
            if self.point_in_triangle(vertex, prev, curr, next_vertex):
                return False
        return True
    
    def point_in_triangle(self, p, a, b, c):
        """Check if point p is inside triangle abc."""
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)

    def ear_clipping_triangulation(self):
        """Triangulate polygon using ear clipping method."""
        vertices = self.vertices.tolist()
        triangles = []
        
        # Continue until we have a triangle
        while len(vertices) > 3:
            n = len(vertices)
            i = 0
            found_ear = False
            
            # Look for an ear
            while i < n and not found_ear:
                if self.is_ear(vertices, i):
                    # Add triangle to triangulation
                    prev = vertices[(i-1) % n]
                    curr = vertices[i]
                    next_vertex = vertices[(i+1) % n]
                    triangles.append([prev, curr, next_vertex])
                    
                    # Remove ear vertex
                    vertices.pop(i)
                    found_ear = True
                else:
                    i += 1
            
            if not found_ear:
                raise ValueError("Could not find an ear in polygon")
        
        # Add the final triangle
        triangles.append(vertices)
        return triangles

    def vertex_to_key(self, vertex):
        """Convert vertex coordinates to a string key."""
        return f"{vertex[0]},{vertex[1]}"
    
    def key_to_vertex(self, key):
        """Convert string key back to vertex coordinates."""
        x, y = map(float, key.split(','))
        return (x, y)

    def three_coloring(self, triangulation):
        """Implement 3-coloring of the triangulation."""
        # Initialize colors dictionary using vertex keys
        self.colors = {self.vertex_to_key(tuple(v)): -1 for v in self.vertices}
        
        # Color first triangle
        first_triangle = triangulation[0]
        for i, vertex in enumerate(first_triangle):
            vertex_key = self.vertex_to_key(tuple(vertex))
            self.colors[vertex_key] = i % 3
        
        # Color remaining vertices
        for triangle in triangulation[1:]:
            for vertex in triangle:
                vertex_key = self.vertex_to_key(tuple(vertex))
                if self.colors[vertex_key] == -1:
                    # Find used colors in this triangle
                    used_colors = set()
                    for v in triangle:
                        v_key = self.vertex_to_key(tuple(v))
                        if self.colors[v_key] != -1:
                            used_colors.add(self.colors[v_key])
                    # Assign first unused color
                    for color in range(3):
                        if color not in used_colors:
                            self.colors[vertex_key] = color
                            break

    def place_guards(self):
        """Place guards on vertices of the same color that covers the polygon."""
        # Count vertices of each color
        color_counts = [0, 0, 0]
        for color in self.colors.values():
            if color != -1:
                color_counts[color] += 1
        
        # Choose color with minimum vertices
        min_color = color_counts.index(min(color_counts))
        
        # Place guards on vertices of chosen color
        self.guards = []
        for vertex_key, color in self.colors.items():
            if color == min_color:
                vertex = self.key_to_vertex(vertex_key)
                self.guards.append(vertex)

    def add_vertex_labels(self):
        """Add vertex labels with coordinates to the plot."""
        for i, vertex in enumerate(self.vertices):
            label = f'{self.vertex_names[i]}\n({vertex[0]}, {vertex[1]})'
            # Offset the label slightly from the vertex
            offset = 5
            if vertex[1] > 0:
                y_offset = offset
            else:
                y_offset = -offset
            if vertex[0] > 0:
                x_offset = offset
            else:
                x_offset = -offset
            
            self.ax.annotate(label, 
                           (vertex[0], vertex[1]),
                           xytext=(vertex[0] + x_offset, vertex[1] + y_offset),
                           ha='center',
                           va='center',
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.7),
                           fontsize=8)

    def animate(self, frame):
        """Animation function for visualization."""
        self.ax.clear()
        
        # Set consistent plot limits
        self.ax.set_xlim(min(v[0] for v in self.vertices) - 20, 
                        max(v[0] for v in self.vertices) + 20)
        self.ax.set_ylim(min(v[1] for v in self.vertices) - 20, 
                        max(v[1] for v in self.vertices) + 20)
        
        if frame == 0:
            # Draw original polygon
            polygon = Polygon(self.vertices, fill=False, color='black')
            self.ax.add_patch(polygon)
            self.add_vertex_labels()
            self.ax.set_title('Original Polygon')
            
        elif frame <= len(self.triangulation):
            # Draw triangulation progress
            polygon = Polygon(self.vertices, fill=False, color='black')
            self.ax.add_patch(polygon)
            
            for i in range(frame):
                triangle = self.triangulation[i]
                tri = Polygon(triangle, fill=False, color='blue', alpha=0.5)
                self.ax.add_patch(tri)
            self.add_vertex_labels()
            self.ax.set_title(f'Triangulation (Step {frame}/{len(self.triangulation)})')
            
        elif frame <= len(self.triangulation) + 1:
            # Draw colored vertices
            polygon = Polygon(self.vertices, fill=False, color='black')
            self.ax.add_patch(polygon)
            
            # Draw all triangles
            for triangle in self.triangulation:
                tri = Polygon(triangle, fill=False, color='blue', alpha=0.5)
                self.ax.add_patch(tri)
            
            # Draw colored vertices
            colors = ['red', 'green', 'blue']
            for vertex in self.vertices:
                vertex_key = self.vertex_to_key(tuple(vertex))
                color_idx = self.colors[vertex_key]
                if color_idx != -1:
                    self.ax.plot(vertex[0], vertex[1], 'o', 
                               color=colors[color_idx], markersize=10)
            
            self.add_vertex_labels()
            self.ax.set_title('3-Coloring')
            
        else:
            # Draw final state with guards
            polygon = Polygon(self.vertices, fill=False, color='black')
            self.ax.add_patch(polygon)
            
            # Draw triangulation
            for triangle in self.triangulation:
                tri = Polygon(triangle, fill=False, color='blue', alpha=0.5)
                self.ax.add_patch(tri)
            
            # Draw colored vertices
            colors = ['red', 'green', 'blue']
            for vertex in self.vertices:
                vertex_key = self.vertex_to_key(tuple(vertex))
                color_idx = self.colors[vertex_key]
                if color_idx != -1:
                    self.ax.plot(vertex[0], vertex[1], 'o', 
                               color=colors[color_idx], markersize=10)
            
            # Draw guards
            for guard in self.guards:
                self.ax.plot(guard[0], guard[1], '*', color='yellow', 
                           markersize=20, markeredgecolor='black')
            
            self.add_vertex_labels()
            self.ax.set_title('Guard Placement')

    def solve(self, save_gif=True, gif_filename='art_gallery.gif'):
        """Solve the Art Gallery Problem and create animation."""
        # Perform triangulation
        self.triangulation = self.ear_clipping_triangulation()
        
        # Perform 3-coloring
        self.three_coloring(self.triangulation)
        
        # Place guards
        self.place_guards()
        
        # Create animation
        frames = len(self.triangulation) + 3  # Original + triangulation steps + coloring + guards
        anim = FuncAnimation(self.fig, self.animate, frames=frames, 
                           interval=500, repeat=False)
        
        # Save as GIF if requested
        if save_gif:
            writer = PillowWriter(fps=2)
            anim.save(gif_filename, writer=writer)
            print(f"Animation saved as {gif_filename}")
        
        plt.show()

# Example usage
polygon = [
    (-70, 40),   # D
    (-50, 60),   # B
    (40, 40),    # A'
    (60, 40),    # C'
    (90, 60),    # E
    (110, 60),   # F
    (110, -60),  # F'
    (90, -60),   # E'
    (60, -40),   # C
    (40, -40),   # A
    (-50, -60),  # B'
    (-70, -40)   # D'
]

polygon = [
    (40, -40),   # P1
    (-50, 60),   # P2
    (60, -40),   # P3
    (-70, 40),   # P4
    (90, 60),    # P5
    (110, 60),   # P6
    (110, -60),  # P7
    (90, -60),   # P8
    (-70, -40),  # P9
    (60, 40),    # P10
    (-50, -60),  # P11
    (40, 40)     # P12
]

vertex_names = ['D', 'B', "A'", "C'", 'E', 'F', "F'", "E'", 'C', 'A', "B'", "D'"]

art_gallery = ArtGalleryProblem(polygon, vertex_names)
art_gallery.solve(save_gif=True, gif_filename='iregular.gif')
