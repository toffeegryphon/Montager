from PIL import Image
import random
from contextlib import suppress
from math import sqrt

# Source Image
source = Image.open("test/test.jpg")

# Source Image Dimensions
width, height = source.size
original = (width, height)

# Pixel Density (Sqrt of Pixels of Source per Pixel of Result)
density = 4

# Result Image Dimensions
size = (400, 400)

# Minimum Euclidean Distance between Top Left corner of each Result Image
closeness = 100

# Number of Images to be Generated
n = 20

# Rate of Image Flash (Images per Second)
rate = 10

# Duration of Whole Montage
duration = int(n / rate)

# Generate n number of Random points within Source Image Bounds
corners = [(random.randint(0, original[0] - size[0]*density), random.randint(0, original[1] - size[1]*density)) for _ in range(n)]

# Checking for closeness
# O(n) of n**2, can be improved
def check(points: list):
    axis = 0 # 0: X, 1: Y
    while axis < 2:
        points.sort(key=lambda x: x[axis])
        i = 0
        while i < n:
            # Euclidean Distance > closeness if and only if Manhattan Distance > closeness
            if points[i][axis] < points[i-1][axis] + closeness:
                x = points[i][0] - points[i-1][0]
                y = points[i][1] - points[i-1][1]
                z = int(sqrt(x**2 + y**2))
                # Remove points if too close
                if z < closeness:
                    corners.remove(points[i])
                    points.pop(i)
            i += 1
        axis += 1
    return points

# Check for closeness once
points = corners
points = check(points)
print(len(points))

# Create Result Images (Frames) and put into List
frames = []
for point in corners:
    frame = source.crop((point[0], point[1], point[0] + size[0]*density, point[1] + size[1]*density))
    frame = frame.resize((size[0], size[1]), Image.ANTIALIAS)
    frames.append(frame)

frames[0].save("test/result.gif", format="GIF", append_images=frames[1:], save_all=True, duration=duration, loop=0)
