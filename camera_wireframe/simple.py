import numpy as np
import open3d as o3d
import time

def create_camera_wireframe():
    # Camera wireframe vertices
    vertices = [
        [0, 0, 0],  # Camera center
        [1, 1, 2],  # Top-right
        [1, -1, 2],  # Bottom-right
        [-1, -1, 2],  # Bottom-left
        [-1, 1, 2],  # Top-left
    ]
    
    # Camera wireframe edges
    edges = [
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 4],
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 1],
    ]

    # Convert vertices and edges to Open3D format
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(vertices)
    line_set.lines = o3d.utility.Vector2iVector(edges)
    line_set.colors = o3d.utility.Vector3dVector([(1, 0, 0) for _ in range(len(edges))])
    
    return line_set

def draw_camera_wireframe():
    camera_wireframe = create_camera_wireframe()
    o3d.visualization.draw_geometries([camera_wireframe])

def animate_camera_wireframe():
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    camera_wireframe = create_camera_wireframe()

    vis.add_geometry(camera_wireframe)

    for i in range(100):
        R = camera_wireframe.get_rotation_matrix_from_xyz((np.pi / 100, 0, 0))
        camera_wireframe.rotate(R, center=camera_wireframe.get_center())
        vis.update_geometry(camera_wireframe)
        vis.poll_events()
        vis.update_renderer()
        time.sleep(0.05)

    vis.destroy_window()

if __name__ == "__main__":
    draw_camera_wireframe()
