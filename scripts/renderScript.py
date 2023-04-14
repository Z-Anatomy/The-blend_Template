import bpy


# Set the render engine to use (optional, defaults to "BLENDER_EEVEE")
bpy.context.scene.render.engine = "BLENDER_EEVEE"
bpy.context.scene.render.image_settings.file_format = "PNG"

# Set the resolution of the output image (optional, defaults to 1920x1080)
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Set the camera to use for rendering (optional, defaults to the active camera)
camera = bpy.data.objects["Camera"]
bpy.context.scene.camera = camera

bpy.context.scene.render.filepath = "//data.png"

# Render the current camera view as an image
bpy.ops.render.render(write_still=True, use_viewport=True)
