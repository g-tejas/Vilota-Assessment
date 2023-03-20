import numpy as np
import matplotlib.pyplot as plt
from spatialmath.base import *
from spatialmath.base import rpy2tr
from spatialmath import *
import matplotlib.animation as animation
import roboticstoolbox.tools.trajectory as tr

# plot_cube is passed the resulting pose from the update function
# T represents a homogeneous transformation matrix, 4x4 because it contains
# both a rotation and a translation matrix
# the R | T, and the bottom row is  0 ... 0 1
# R is the rotation matrix and T is the translation vector
# Default T is origin and axis oriented
def plot_cube(ax, T=SE3()):
    # All coordinates of the 8 vertices of a 3D cube centered around origin
    P = np.array([
            [-1, 1, 1, -1, -1, 1, 1, -1],
            [-1, -1, 1, 1, -1, -1, 1, 1],
            [-1, -1, -1, -1, 1, 1, 1, 1]])

    # Apply SE3() transformation matrix to the points
    # Q now contains the transformed points in 3D space
    Q = T*P

    setup_axis(ax)

    # Contain the lines of the cubes edges for plt to plot
    lines = [[0, 1, 5, 6], [1, 2, 6, 7], [2, 3, 7, 4], [3, 0, 4, 5]]
    ret = []
    for line in lines:
        o=ax.plot(Q[0, line], Q[1, line], Q[2, line])
        ret.append(o[0])
    return ret

# Ensure the cube is visible in the plot
def setup_axis(ax):
    ax.set_xlim3d(-5, 5)
    ax.set_ylim3d(0, 10)
    ax.set_zlim3d(-5, 5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

# idx: Select joint config from the out.q array
def update_frame(idx):
    global out

    # Create a pure translation matrix, 5 units along x axis and 5 along z-axix
    M1 = SE3(5,0,5)

    # Create an SE(3) 4x4 rotation matrix from roll-pitch-yaw angles
    # Rotate around z, then y and last x.
    # The rpy2tr converts the joint configuration (rpy angles) to a 4x4 matrix
    # that determines the position and orientation of the cube for the current
    # joint configuration to be used by the animation
    M2 = SE3(rpy2tr(out.q[idx]))

    # Matrix Composition, since the * operator is overloaded
    # Compose the homogeneous matrix (from joint config) with the pure translation matrix
    M2 *= M1
    return plot_cube(ax, M2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 3-DOF
# Initial joint coordinate
q0 = np.array([0, 0, 0])
# Final joint coordinate
qf = np.array([-np.pi/4, np.pi/2, np.pi/2])

# Must be global, since update_frame needs to access the trajectory information (position and orientation)
# for each frame of the animation. 
# Generates linear interpolation between q0 and qf for the cube rotation animation
# Takes t=100 number of steps
out = tr.jtraj(q0, qf, t=100)
number_of_steps = len(out.q)

# In each frame of the animation, update_frame is called with the current joint
# config (ith frame) of the animation, and the plot_cube generates the corresponding
# pose of the rotating cube.
anim = animation.FuncAnimation(fig, update_frame,
                              frames=number_of_steps,
                              interval=40,
                              blit=True,
                              repeat=True)

plt.show()
