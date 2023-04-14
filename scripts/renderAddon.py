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


class SetActiveCameraOperator(bpy.types.Operator):
    """Set the selected camera as the active camera"""
    bl_idname = "render.set_active_camera"
    bl_label = "Set Active Camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_object = context.view_layer.objects.active
        if active_object is None or active_object.type != 'CAMERA':
            self.report({'ERROR'}, "No camera selected")
            return {'CANCELLED'}

        context.scene.camera = active_object
        self.report({'INFO'}, "Camera set as active")
        return {'FINISHED'}


class RenderImageOperator(bpy.types.Operator):
    """Render the current camera view as an image"""
    bl_idname = "render.render_image"
    bl_label = "Render Image"

    def filePathUpdate(self, context):
        context.scene.render.filepath = self.filepath

    filepath: bpy.props.StringProperty(
        name="FilePath",
        description="Enter the file path where the image should be saved",
        subtype="FILE_PATH",
        default="/Users/coolhead/Desktop/render.png",
        update=filePathUpdate
    )

    def execute(self, context):
        # Set the render engine to use (optional, defaults to "BLENDER_EEVEE")
        context.scene.render.engine = "BLENDER_EEVEE"
        context.scene.render.image_settings.file_format = "PNG"

        # Set the resolution of the output image (optional, defaults to 1920x1080)
        context.scene.render.resolution_x = 1920
        context.scene.render.resolution_y = 1080

        # Set the camera to use for rendering (optional, defaults to the active camera)
        camera = context.scene.camera
        # context.scene.render.filepath = self.filepath

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
        row.prop(context.scene.render, "filepath", text="File Format")

        row = layout.row()
        row.operator("render.render_image",
                     text="Render Image")
        row = layout.row()
        row.operator("render.set_active_camera", text="Set Active Camera")


classes = [
    RenderImageOperator,
    RenderImagePanel,
    SetActiveCameraOperator
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
