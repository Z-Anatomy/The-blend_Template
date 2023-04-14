import bpy


bl_info = {
    "name": "Render Image",
    "author": "Pratik Sharma(@biomathcode)",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "",
    "description": "Render Image in the ViewPort of the Camera",
    "warning": "Render the View of the Camera Object",
    "wiki_url": "",
    "category": "Render",
}


class RenderImageOperator(bpy.types.Operator):
    """Render the current camera view as an image"""
    bl_idname = "render.render_image"
    bl_label = "Render Image"

    file_format: bpy.props.EnumProperty(
        name="File Format",
        items=[('PNG', 'PNG', 'Portable Network Graphics'),
               ('JPEG', 'JPEG', 'Joint Photographic Experts Group'),
               ('BMP', 'BMP', 'Bitmap')],
        default='PNG'
    )
    camera: bpy.props.StringProperty(
        name="Camera",
        default="Camera"
    )

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Enter the file path where the image should be saved",
        subtype="FILE_PATH",
        default="/Users/coolhead/Desktop/render.png",
    )

    def execute(self, context):
        # Set the render engine to use (optional, defaults to "BLENDER_EEVEE")
        context.scene.render.engine = "BLENDER_EEVEE"
        context.scene.render.image_settings.file_format = self.file_format

        # Set the resolution of the output image (optional, defaults to 1920x1080)
        context.scene.render.resolution_x = 1920
        context.scene.render.resolution_y = 1080

        # Set the camera to use for rendering (optional, defaults to the active camera)
        camera = context.scene.camera
        context.scene.render.filepath = self.filepath

        # Render the current camera view as an image
        bpy.ops.render.render(write_still=True, use_viewport=True)

        return {'FINISHED'}


class RenderImagePanel(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'Render Image'
    bl_category = 'Render'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene.render, "filepath", text="File Path")
        row = layout.row()
        row.prop(context.scene.render,
                 "image_settings.file_format", text="File Format")
        row = layout.row()
        row.operator("render.render_image",
                     text="Render Image")


classes = [
    RenderImageOperator,
    RenderImagePanel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
