##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class VIEW3D_MT_actor_add(bpy.types.Menu):
    """The OpenGoal actor menu"""

    bl_label = "Actor"
    bl_idname = "VIEW3D_MT_actor_add"

    def draw(self, context):

        pass


classes.append(VIEW3D_MT_actor_add)  # Add the class to the array


class ActorSpawnButton(bpy.types.Operator):
    """Creates an actor mesh"""  # Be careful, this docstring is exposed to the user

    bl_idname = "object.move_x"  # Unique operator reference name
    bl_label = "Actor"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    def __init__(self):  # __init__() is called when creating the operator

        pass

    def execute(self, context):  # execute() is called when running the operator

        for obj in context.scene.objects:
            obj.location.x += 1.0

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(ActorSpawnButton)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


def draw_actor_menu(self, context):
    """Draws the "add actors" menu"""

    self.layout.menu(VIEW3D_MT_actor_add.bl_idname, icon="ERROR")


def draw_buttons(self, context):
    """Draws the buttons within the "add actors" menu"""  # Eventually this will be automated when a new actor instance is created

    def label(txt, icn):
        self.layout.label(text=txt, icon=icn)

    def button(txt, icn):
        self.layout.operator(ActorSpawnButton.bl_idname, text=txt, icon=icn)

    label("Collectables", "WORLD_DATA")

    button("Power Cell", "ERROR")
    button("Precursor Orb", "ERROR")
    button("Scout Fly", "ERROR")
    button("Green Eco", "ERROR")
    button("Blue Eco", "ERROR")
    button("Yellow Eco", "ERROR")
    button("Red Eco", "ERROR")

    label("Crates", "WORLD_DATA")

    button("Wooden Crate", "ERROR")
    button("Metal Crate", "ERROR")
    button("Scout Fly Box", "ERROR")
    button("Bucket", "ERROR")

    label("Other", "WORLD_DATA")

    button("Death Plane", "ERROR")
    button("Checkpoint", "ERROR")
    button("Load Boundary", "ERROR")


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    # Add the "add actor" menu
    bpy.types.VIEW3D_MT_add.prepend(draw_actor_menu)

    # Add buttons to the "add actor" menu
    bpy.types.VIEW3D_MT_actor_add.append(draw_buttons)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    # Remove buttons from the "add actor" menu
    bpy.types.VIEW3D_MT_actor_add.remove(draw_buttons)

    # Remove the "add actor" menu
    bpy.types.VIEW3D_MT_add.remove(draw_actor_menu)


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
