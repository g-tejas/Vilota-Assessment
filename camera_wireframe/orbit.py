import numpy as np
import open3d as o3d
import time

# Function to create a camera wireframe
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

def create_cube(center, size):
    cube = o3d.geometry.TriangleMesh.create_box(width=size, height=size, depth=size)
    cube.translate(center - np.array([size/2, size/2, size/2]))
    cube.paint_uniform_color([0.5, 0.5, 0.5])
    return cube


def visualize_pose():
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    object_center = np.array([0, 0, 0.5])  # Place the cube directly above the plane
    object_size = 1
    floor_height = -0.5 # Adjust the floor height accordingly
    camera_wireframe = create_camera_wireframe()
    cube = create_cube(object_center, object_size)

    floor = o3d.geometry.TriangleMesh.create_box(width=10, height=0.01, depth=10)
    floor.translate([-5, floor_height, -5])  # Translate the floor to center the cube
    floor.paint_uniform_color([0.1, 0.1, 0.1])

    cube.paint_uniform_color([0.2, 0.5, 0.3])

    # Add the shapes into the visualisation
    vis.add_geometry(camera_wireframe)
    vis.add_geometry(cube)
    vis.add_geometry(floor)

    view_control = vis.get_view_control()
    view_control.set_lookat(object_center)
    view_control.set_up([0, 0, 1])
    view_control.set_front([0, -1, 0])
    view_control.set_zoom(1.5)

    # Place the camera wireframe in a fixed position pointing towards the cube
    x = 5
    y = -5
    z = 3
    camera_wireframe.translate([-x, -y, -z], relative=False)

    # Compute the rotation matrix to keep the camera pointing towards the cube
    direction = object_center - np.array([-x, -y, -z], dtype=float)  # Convert to float
    direction /= np.linalg.norm(direction)
    right = np.cross([0, 0, 1], direction)
    right /= np.linalg.norm(right)
    up = np.cross(direction, right)
    R = np.column_stack((right, up, direction))

    camera_wireframe.rotate(R, center=camera_wireframe.get_center())

    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    visualize_pose()
