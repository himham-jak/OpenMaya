# TODO: docstring


##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy


##############################################################################
# Constants
##############################################################################


##############################################################################
# Properties and Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class ObjectMoveX(bpy.types.Operator):
    """Move all objects in the scene by one unit in the x direction."""

    bl_idname = "object.move_x"  # Unique operator reference name
    bl_label = "Move X by One"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    def execute(self, context):  # execute() is called when running the operator

        for obj in context.scene.objects:
            obj.location.x += 1.0

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(ObjectMoveX)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


def menu_func(self, context):
    self.layout.operator(ObjectMoveX.bl_idname)


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    # bpy.types.VIEW3D_MT_object.append(menu_func)  # Add operators to an existing menu


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
