##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class OBJECT_PT_LevelEditorMenu(bpy.types.Panel):
    """"""

    bl_idname = "OBJECT_PT_LevelEditorMenu"
    bl_label = "Level Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level Editor"
    bl_context = "objectmode"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        layout.label(text="Test", icon="ERROR")
        layout.separator()


classes.append(OBJECT_PT_LevelEditorMenu)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
