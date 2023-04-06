import bpy
from mathutils import Vector
import mathutils
from bpy_extras.object_utils import object_data_add


class OBJECT_OT_make_label(bpy.types.Operator):
    """Make label\n 1.Select vertex in Edit Mode\n 2. Open text in Text Editor"""
    bl_idname = "object.make_label"
    bl_label = "Make Label"
    bl_options = {'REGISTER', 'UNDO'}

    use_custom_label: bpy.props.BoolProperty(
        default=False, name="Use custom property")
    custom_label: bpy.props.StringProperty(default="Custom Label")

    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_MESH', 'OBJECT'} and context.object is not None

    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)

    def execute(self, context):
        # OPTIONS
        font_radius = 0.003  # size of font
        font_x_align = 'CENTER'
        # line_thickness = 0.0002
        line_offset = 0.0015  # distance between label and line
        #

        bpy.ops.object.mode_set(mode='OBJECT')
        selected_verts = [v for v in context.object.data.vertices if v.select]
        if len(selected_verts) != 1:
            self.report(type={"ERROR"}, message="Select one vertex.")
            return {"CANCELLED"}

        active_object = context.object

        vert_co = active_object.matrix_world @ Vector(selected_verts[0].co)
        text_co = vert_co.copy()
        text_co.z += 0.05

        line_end_co = vert_co.copy()

        text_name = self.custom_label
        if not self.use_custom_label:
            for area in bpy.context.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    for space in area.spaces:
                        if space.type == 'TEXT_EDITOR':
                            text_name = space.text.name

        bpy.ops.object.text_add(radius=font_radius, enter_editmode=False, align='WORLD',
                                location=text_co, rotation=(1.5708, 0, 0), scale=(1, 1, 1))
        font_object = context.object
        font_object.name = f"{text_name}.t"
        font_object.data.name = font_object.name
        font_object.data.body = text_name.upper()
        font_object.data.align_x = font_x_align
        try:
            font_object.data.font_bold = bpy.data.fonts["DejaVuSansCondensed"]
        except:
            self.report(
                type={"WARNING"}, message="Font DejaVuSansCondensed not found. Add it manualy.")

        # Get material
        mat = bpy.data.materials.get("Text")
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name="Text")

        # Assign it to object
        font_object.data.materials.append(mat)

        # context.collection.objects.link(font_object)
        context.collection.objects.unlink(font_object)
        # bpy.data.collections['0:Labels'].objects.link(font_object)
        try:
            for col in active_object.users_collection:
                col.objects.link(font_object)
        except:
            pass
        print(active_object, font_object)

        # Mesh
        verts = [text_co-Vector((0, 0, line_offset)), line_end_co]
        edges = [[0, 1]]
        faces = []
        mesh = bpy.data.meshes.new(name=f"{text_name}.j")
        mesh.from_pydata(verts, edges, faces)
        # useful for development when the mesh may be invalid.
        # mesh.validate(verbose=True)

        old_cursor_loc = context.scene.cursor.location.copy()
        context.scene.cursor.location = (0, 0, 0)
        line_object = object_data_add(context, mesh)
        context.scene.cursor.location = old_cursor_loc
        line_object.hide_select = True
        line_object.show_wire = True

        context.collection.objects.unlink(line_object)
        # bpy.data.collections['0:Labels'].objects.link(line_object)
        try:
            for col in active_object.users_collection:
                col.objects.link(line_object)
        except:
            pass

        # translate origin
        line_object.data.transform(mathutils.Matrix.Translation(-text_co))
        line_object.matrix_world.translation += text_co

        # set parent inverse (line <- font)
        line_object.parent = font_object
        line_object.matrix_parent_inverse = font_object.matrix_world.inverted()

        # set parent inverse (font <- element)
        font_object.parent = active_object
        font_object.matrix_parent_inverse = active_object.matrix_world.inverted()

        font_object.delta_location = font_object.delta_location + font_object.location
        font_object.location = (0, 0, 0)

        # Add Hook modifier
        hm = line_object.modifiers.new(
            name=f"Hook",
            type='HOOK',
        )
        hm.object = active_object
        hm.vertex_indices_set([1])

        # Add Skin modifier
        # line_object.modifiers.new(name='Skin', type='SKIN')
        # for v in line_object.data.skin_vertices[0].data:
        #     v.radius = [line_thickness] * 2

        context.view_layer.objects.active = font_object
        font_object.select_set(True)
        font_object.hide_set(False)
        return {"FINISHED"}
