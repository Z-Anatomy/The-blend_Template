import bpy

# Get all objects in the scene
all_objects = bpy.context.scene.objects

# Iterate over all objects and find those with the ".s" suffix
for obj in all_objects:
    if obj.name.endswith(".s"):
        obj.scale[0] = -1
        obj.scale[1] = -1
        obj.scale[2] = -1
        obj.delta_scale[0] = 1
        obj.delta_rotation_quaternion[0] = 0
