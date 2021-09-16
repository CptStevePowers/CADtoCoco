import os, sys
s_path = os.path.dirname(os.path.dirname(__file__))
print(s_path)
sys.path.append(s_path)

import blender_util, math_util

points = math_util.point_sphere()

for point in points:
    cam = blender_util.new_camera()
    cam.location = point
    blender_util.update_camera(cam)