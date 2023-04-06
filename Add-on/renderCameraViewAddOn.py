import bpy


class RenderImageOperator(bpy.types.Operator):
    """Render the current camera view as an image"""
    bl_idname = "render.render_image"
    bl_label = "Render Image"

    def execute(self, context):
        # Set the render engine to use (optional, defaults to "BLENDER_EEVEE")
        context.scene.render.engine = "BLENDER_EEVEE"
        context.scene.render.image_settings.file_format = "PNG"

        # Set the resolution of the output image (optional, defaults to 1920x1080)
        context.scene.render.resolution_x = 1920
        context.scene.render.resolution_y = 1080

        # Set the camera to use for rendering (optional, defaults to the active camera)
        camera = bpy.data.objects["Camera"]
        context.scene.camera = camera

        context.scene.render.filepath = "//data.png"

        # Render the current camera view as an image
        bpy.ops.render.render(write_still=True, use_viewport=True)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(RenderImageOperator)


def unregister():
    bpy.utils.unregister_class(RenderImageOperator)


if __name__ == "__main__":
    register()
