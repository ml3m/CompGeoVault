# solve for the exercise 3 -> where we can't do 3 triangles with 5 edges, but
# we take the possible example with 3 triangles and 7 edges. that can be 3-colored 
from class_usable import ArtGalleryProblem
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation, PillowWriter
from typing import List, Tuple

class ArtGalleryProblemTwoCameras(ArtGalleryProblem):
    def __init__(self, polygon_vertices: List[Tuple[float, float]], vertex_names=None):
        super().__init__(polygon_vertices, vertex_names)
    
    def place_guards_two_cameras(self):
        """Place exactly two guards on vertices that provide good coverage."""
        max_distance = 0
        guard_positions = []
        
        for i, v1 in enumerate(self.vertices):
            for j, v2 in enumerate(self.vertices[i+1:], i+1):
                dist = np.linalg.norm(np.array(v1) - np.array(v2))
                if dist > max_distance:
                    max_distance = dist
                    guard_positions = [tuple(v1), tuple(v2)]
        
        self.guards = guard_positions

    def animate(self, frame):
        """Modified animation function to show only stars on blue vertices."""
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
            
        else:
            # Draw final state
            polygon = Polygon(self.vertices, fill=False, color='black')
            self.ax.add_patch(polygon)
            
            # Draw triangulation
            for triangle in self.triangulation:
                tri = Polygon(triangle, fill=False, color='blue', alpha=0.5)
                self.ax.add_patch(tri)
            
            # Draw vertices - stars for blue, dots for others
            colors = ['red', 'green', 'blue']
            for vertex in self.vertices:
                vertex_key = self.vertex_to_key(tuple(vertex))
                color_idx = self.colors[vertex_key]
                if color_idx != -1:
                    if color_idx == 3213:  # Blue color index
                        self.ax.plot(vertex[0], vertex[1], '*', 
                                   color='yellow', markersize=15, 
                                   markeredgecolor='black')
                    else:
                        self.ax.plot(vertex[0], vertex[1], 'o', 
                                   color=colors[color_idx], markersize=10)
            
            self.add_vertex_labels()
            self.ax.set_title('Vertices with Stars for Blue Color')
    
    def solve(self, save_gif=True, gif_filename='art_gallery_two_cameras.gif'):
        """Solve the Art Gallery Problem with visualization of blue vertices as stars."""
        # Perform triangulation
        self.triangulation = self.ear_clipping_triangulation()
        
        # Perform 3-coloring
        self.three_coloring(self.triangulation)
        
        # Place guards (but won't display them)
        self.place_guards_two_cameras()
        
        # Create animation
        frames = len(self.triangulation) + 2  # Reduced by 1 since we combined final states
        anim = FuncAnimation(self.fig, self.animate, frames=frames, 
                           interval=500, repeat=False)
        
        if save_gif:
            writer = PillowWriter(fps=2)
            anim.save(gif_filename, writer=writer)
            print(f"Animation saved as {gif_filename}")
        
        plt.show()

# Example usage
polygon = [
        (-80,40),# A    
        (-90,10),# C
        (-60,20),# D
        (-40,30),# B
        (-30,40) # E
]

vertex_names = ['P1', 'P3', 'P2', 'P4', 'P6', 'P5']

art_gallery = ArtGalleryProblemTwoCameras(polygon, vertex_names)
art_gallery.solve(save_gif=True, gif_filename='irregular_two_cameras.gif')
