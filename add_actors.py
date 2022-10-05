##############################################################################
# Imports
##############################################################################


import bpy
import abc

##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class ActorSpawnButton(bpy.types.operator, ABC):
    """Creates an actor mesh."""

    bl_idname = "object.move_x"  # Unique operator reference name
    bl_label = "Precursor Orb"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    def __init__(self):  # __init__() is called when creating the operator
        pass

    def execute(self, context):  # execute() is called when running the operator

        for obj in context.scene.objects:
            obj.location.x += 1.0

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(ActorSpawnButton)  # Add the class to the array

class OrbSpawnButton(ActorSpawnButton):
    """Creates an actor mesh."""

    bl_idname = "object.move_x"  # Unique operator reference name
    bl_label = "Precursor Orb"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    def __init__(self):  # __init__() is called when creating the operator
        pass

    def execute(self, context):  # execute() is called when running the operator

        for obj in context.scene.objects:
            obj.location.x += 1.0

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(OrbSpawnButton)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


def menu_func(self, context):
    self.layout.operator(ActorSpawnButton.bl_idname)
    self.layout.operator(OrbSpawnButton.bl_idname)

##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_mesh_add.append(
        menu_func
    )  # Add operators to the existing add mesh menu


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_mesh_add.remove(
        menu_func
    )  # Remove operators to the existing add mesh menu


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
