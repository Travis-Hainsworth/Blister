import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Example data (replace with your own)
time = np.arange(0, 10, 0.1)
compression = np.sin(time)  # Example compression values
marker_colors = ['blue', 'green', 'red', 'cyan', 'magenta']  # Example marker colors

# Animation settings
fps = 30  # Frames per second
interval = 1000 / fps  # Delay between frames (in milliseconds)

# Create the figure and axis
fig, ax = plt.subplots()

# Set the axis limits
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Initialize the markers
markers = ax.plot([], [], '.', markersize=18)

# Set the axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Set the title
title = ax.set_title('t = 0 (s)')


# Function to update the animation frame
def update(frame):
    # Example points (replace with your own)
    points = np.random.rand(5, 2)  # Random points in 2D

    # Calculate the new marker colors based on the compression value
    color_scale = compression[frame]  # Example scaling factor for marker color
    color_scale_array = np.full(len(marker_colors), color_scale, dtype=np.float64)
    marker_colors_scaled = [tuple(color_scale_array * np.array(marker_color)) for marker_color in marker_colors]

    # Update the marker positions and colors
    for marker, color in zip(markers, marker_colors_scaled):
        marker.set_data(points[:, 0], points[:, 1])
        marker.set_color(color)

    # Update the title
    title.set_text('t = {:.1f} (s)'.format(time[frame]))

    return markers, title


# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(time), interval=interval, blit=True)

# Show the plot
plt.show()
