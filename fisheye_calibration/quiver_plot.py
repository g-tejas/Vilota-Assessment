import numpy as np
import matplotlib.pyplot as plt

# KB4 parameters
params = [622, 622, 965, 631, -0.256, -0.0015, 0.0007, -0.0002]
fx, fy, cx, cy, k1, k2, k3, k4 = params
width, height = 1920, 1200

# Create a grid of points
num_points = 20
x = np.linspace(0, width, num_points)
y = np.linspace(0, height, num_points)
X, Y = np.meshgrid(x, y)

# Normalize the points to the camera coordinate system
x_normalized = (X - cx) / fx
y_normalized = (Y - cy) / fy

# Calculate the distorted points
r = np.sqrt(x_normalized**2 + y_normalized**2)
theta = np.arctan(r)
theta_distorted = theta * (1 + k1*theta**2 + k2*theta**4 + k3*theta**6 + k4*theta**8)
x_distorted = x_normalized * theta_distorted / r
y_distorted = y_normalized * theta_distorted / r

# Convert back to pixel coordinates
X_distorted = x_distorted * fx + cx
Y_distorted = y_distorted * fy + cy

# Calculate displacement vectors
U = X_distorted - X
V = Y_distorted - Y

# Plot the quiver plot
plt.figure(figsize=(10, 6))
plt.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, width=0.002, color='r', alpha=0.5)
plt.scatter(X, Y, marker='.', color='b', label='Original Points')
plt.scatter(X_distorted, Y_distorted, marker='.', color='r', label='Distorted Points')
plt.legend()
plt.title("Quiver Plot of Distortion")
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

