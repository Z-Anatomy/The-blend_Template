
bl_info = {
    "name": "Object adder", 
    "author":"Pratik Sharma",
    "version": (0, 0, 1), 
    "blender": (3, 2, 0),
    "location" : "View3d > Tool", 
    "warning": "", 
    "wiki_url": "", 
    "category": "Add Mesh",
}


import bpy


class TestPanel(bpy.types.Panel):
    bl_label = "Text Panel"
    bl_idname = "PT_TestPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    bl_category = "Addon"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        
        row.label(text="Sample Text", icon="CUBE")
        row = layout.row()
        row.operator("mesh.primitive_cube_add", icon="CUBE")
        row = layout.row()
        row.operator("mesh.primitive_uv_sphere_add", icon='SPHERE')
        
        row = layout.row()
        
        row.operator("object.text_add")
        

class PanelA(bpy.types.Panel):
    bl_label = "Scaling"
    bl_idname = "Panel_A"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "PT_TestPanel"
    bl_options = {'DEFAULT_CLOSED'}
    
    bl_category = "Addon"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        
        row.label(text="Panel A", icon="FONT_DATA")        


def register():
    bpy.utils.register_class(TestPanel)
    bpy.utils.register_class(PanelA)
    

def unregister():
    bpy.utils.unregister_class(TestPanel)
    bpy.utils.unregister_class(PanelA)
    

if __name__ == "__main__":
    register()

    