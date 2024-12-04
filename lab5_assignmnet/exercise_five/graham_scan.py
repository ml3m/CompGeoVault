import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def andrew_convex_hull(points):
    points = sorted(points)
    lower = []
    steps = []
    
    for p in points:
        while len(lower) >= 2:
            current_step = {
                'points': points.copy(),
                'lower': lower.copy(),
                'current': p,
                'status': 'checking orientation'
            }
            
            if orientation(lower[-2], lower[-1], p) != 2:
                lower.pop()
                current_step['status'] = 'removing point'
            else:
                break
            
            steps.append(current_step)
        
        lower.append(p)
        
        current_step = {
            'points': points.copy(),
            'lower': lower.copy(),
            'current': p,
            'status': 'adding point'
        }
        steps.append(current_step)
    
    return lower, steps

def visualize_convex_hull(save_gif=True):
    points = [(1, 10), (-2, 7), (3, 8), (4, 10), (5, 7), (6, 7), (7, 11)]
    
    lower_hull, steps = andrew_convex_hull(points)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.title("Andrew's Convex Hull Algorithm - Lower Hull")
    
    def update(frame):
        ax.clear()
        step = steps[frame]
        
        x, y = zip(*step['points'])
        ax.scatter(x, y, color='blue', label='Points')
        
        current = step['current']
        ax.scatter(current[0], current[1], color='red', s=100, label='Current Point')
        
        if step['lower']:
            lx, ly = zip(*step['lower'])
            ax.plot(lx, ly, color='green', marker='o', linestyle='-', linewidth=2, label='Lower Hull')
            
            # Create polygon for coloring the area above the lower hull
            max_y = max(y) + 5
            
            polygon_points = step['lower'] + [
                (step['lower'][-1][0], max_y), 
                (step['lower'][0][0], max_y)
            ]
            
            polygon = patches.Polygon(polygon_points, 
                                      facecolor='pink', 
                                      edgecolor='none', 
                                      alpha=0.3)
            ax.add_patch(polygon)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.legend()
        ax.set_title(f"Step {frame+1}: {step['status']}")
        
        plt.grid(True)
    
    frames = len(steps)
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=1000)
    
    if save_gif:
        ani.save('convex_hull.gif', writer='pillow', fps=1)
    
    plt.tight_layout()
    plt.show()

visualize_convex_hull()
