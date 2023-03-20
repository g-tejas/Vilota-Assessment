import numpy as np
import matplotlib.pyplot as plt

# KB4 parameters
params = [622, 622, 965, 631, -0.256, -0.0015, 0.0007, -0.0002]
fx, fy, cx, cy, k1, k2, k3, k4 = params
width, height = 1920, 1200

# Create a grid of points that may represent the calibration plate for example.
num_points = 50
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

# Plot the original and distorted grid
plt.figure(figsize=(12, 7))
plt.subplot(121)
plt.title("Original Grid")
plt.scatter(X, Y, marker='.')
plt.grid(True)

plt.subplot(122)
plt.title("Distorted Grid (KB4 Model)")
plt.scatter(X_distorted, Y_distorted, marker='.')
plt.grid(True)

plt.show()

