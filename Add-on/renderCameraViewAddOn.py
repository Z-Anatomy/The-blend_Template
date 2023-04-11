import bpy


bl_info = {
    "name": "Render Image",
    "author": "Pratik Sharma(@biomathcode)",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "",
    "description": "Render Image in the ViewPort of the Camera",
    "warning": "Render the View of the Camera Object",
    "wiki_url": "https://github.com/Z-Anatomy/blend-template",
    "category": "Add Mesh",

}


class RenderImageOperator(bpy.types.Operator):
    """Render the current camera view as an image"""
    bl_idname = "render.render_image"
    bl_label = "Render Image"

    file_format: bpy.props.EnumProperty(
        items=[("PNG", "PNG", "PNG"), ("JPEG", "JPEG", "JPEG"),
               ("BMP", "BMP", "BMP")],
        name="File Format",
        default="PNG",
    )
    file_path: bpy.props.StringProperty(
        name="File Path", subtype="FILE_PATH", default="//render.png")

    def execute(self, context):
        try:
            # Use context overrides to get the selected camera object
            override = context.copy()
            override["area.type"] = "VIEW_3D"
            override["region.type"] = "WINDOW"
            override["space_data.region_3d.view_perspective"] = "CAMERA"
            camera = context.scene.camera = context.space_data.camera
            if camera is None:
                self.report({"ERROR"}, "No camera selected")
                return {"CANCELLED"}

            # Set the render engine to use (optional, defaults to "BLENDER_EEVEE")
            context.scene.render.engine = "BLENDER_EEVEE"
            context.scene.render.image_settings.file_format = self.file_format

            # Set the resolution of the output image (optional, defaults to 1920x1080)
            context.scene.render.resolution_x = 1920
            context.scene.render.resolution_y = 1080

            # Set the camera to use for rendering
            context.scene.camera = camera

            # Set the filepath for the output image
            context.scene.render.filepath = self.file_path

            # Render the current camera view as an image
            bpy.ops.render.render(
                write_still=True, use_viewport=True, override=override)

            self.report({"INFO"}, "Rendering complete")
            return {"FINISHED"}

        except Exception as e:
            self.report({"ERROR"}, str(e))
            return {"CANCELLED"}


# class RenderImageOperator(bpy.types.Operator):
#     """Render the current camera view as an image"""
#     bl_idname = "render.render_image"
#     bl_label = "Render Image"

#     def execute(self, context):
#         # Set the render engine to use (optional, defaults to "BLENDER_EEVEE")
#         context.scene.render.engine = "BLENDER_EEVEE"
#         context.scene.render.image_settings.file_format = "PNG"

#         # Set the resolution of the output image (optional, defaults to 1920x1080)
#         context.scene.render.resolution_x = 1920
#         context.scene.render.resolution_y = 1080

#         # Set the camera to use for rendering (optional, defaults to the active camera)
#         camera = bpy.data.objects["Camera"]
#         context.scene.camera = camera

#         context.scene.render.filepath = "//data.png"

#         # Render the current camera view as an image
#         bpy.ops.render.render(write_still=True, use_viewport=True)

#         return {'FINISHED'}


class RenderImageView(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_idname = "PT_RenderImage"
    bl_region_type = 'UI'
    bl_label = 'Render Image'
    bl_context = 'objectmode'

    bl_category = 'Render Image'

    def draw(self, context):
        layout = self.layout
        layout.operator("render.render_image")


def register():
    bpy.utils.register_class(RenderImageOperator)
    bpy.utils.register_class(RenderImageView)


def unregister():
    bpy.utils.unregister_class(RenderImageOperator)
    bpy.utils.register_class(RenderImageView)


if __name__ == "__main__":
    register()
