import bpy


class RenderImageOperator(bpy.types.Operator):
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

    file_path: bpy.props.StringProperty(
        name="File Path",
        subtype='FILE_PATH',
        default="//render.png"
    )

    def execute(self, context):
        context.scene.render.engine = "BLENDER_EEVEE"
        context.scene.render.image_settings.file_format = self.file_format

        # Set the resolution of the output image (optional, defaults to 1920x1080)
        context.scene.render.resolution_x = 1920
        context.scene.render.resolution_y = 1080

        # Set the camera to use for rendering (optional, defaults to the active camera)
        camera = context.scene.camera
        context.scene.render.filepath = self.file_path

        # Render the current camera view as an image
        bpy.ops.render.render(write_still=True, use_viewport=True)

        return {'FINISHED'}


class RenderImagePanel(bpy.types.Panel):
    bl_idname = "RENDER_PT_render_image"
    bl_label = "Render Image"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Settings:")

        row = layout.row()
        row.prop_enum(RenderImageOperator.bl_rna_get_subclass(
            RenderImageOperator), "file_format")

        row = layout.row()
        row.prop_search(RenderImageOperator.bl_rna_get_subclass(
            RenderImageOperator), "camera", context.scene, "objects", text="Camera")

        row = layout.row()
        row.prop(RenderImageOperator.bl_rna_get_subclass(
            RenderImageOperator), "file_path")

        row = layout.row()
        row.operator("render.render_image", text="Render")


classes = (RenderImageOperator, RenderImagePanel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
