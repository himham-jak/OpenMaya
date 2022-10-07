##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import os
import json
import bpy.utils.previews


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


# name following the convention of existing menus
class VIEW3D_MT_actor_add(bpy.types.Menu):
    """The "add actor" menu"""

    bl_idname = "VIEW3D_MT_actor_add"
    bl_label = "Actor"

    def draw(self, context):

        pass


classes.append(VIEW3D_MT_actor_add)  # Add the class to the array


class ActorSpawnButton(bpy.types.Operator):
    """Creates an actor mesh"""  # Be careful, this docstring is exposed to the user

    bl_idname = "object.spawn_actor"  # Unique operator reference name
    bl_label = "Actor"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    mesh_name: bpy.props.StringProperty()  # The name of the mesh that needs to be spawned

    def execute(cls, context):  # execute() is called when running the operator

        print(f"Creating Actor: {cls.mesh_name}.glb")

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(ActorSpawnButton)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


custom_icons = bpy.utils.previews.new()


def add_custom_icons():
    """Add the necessary custom icons"""

    # path to the folder where the icon is
    # the path is calculated relative to this py file inside the addon folder
    my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # load a preview thumbnail of a file and store in the previews collection
    for filename in os.listdir(my_icons_dir):
        custom_icons.load(
            filename.split(".")[0], os.path.join(my_icons_dir, filename), "IMAGE"
        )


def draw_actor_menu(self, context):
    """Draws the "add actors" menu"""

    self.layout.menu(
        VIEW3D_MT_actor_add.bl_idname,
        icon_value=custom_icons["open-goal"].icon_id,
    )


def draw_buttons(self, context):
    """Draws the buttons within the "add actors" menu"""  # Eventually this will be automated when a new actor instance is created

    def label(txt, icn, visible=True):
        if visible:
            self.layout.label(text=txt, icon_value=custom_icons[icn].icon_id)

    def button(txt, icn="open-goal", mesh="default", visible=True):
        if visible:
            button = self.layout.operator(
                ActorSpawnButton.bl_idname,
                text=txt,
                icon_value=custom_icons[icn].icon_id,
            )
            button.mesh_name = mesh

    json_path = os.path.join(os.path.dirname(__file__), "actor_types.json")

    # Guard clause throwing an error if json file doesn't exist, replace with try, except eventually
    if not os.path.exists(json_path):
        print("actor_types.json not found")
        return 0

    with open(json_path, "r") as f:
        json_data = json.loads(f.read())

    for category in json_data:
        label(category, json_data[category][0]["Icon"], json_data[category][0]["Show"])

        for i in range(len(json_data[category]) - 1):
            button(
                json_data[category][i + 1]["Text"],
                json_data[category][i + 1]["Icon"],
                json_data[category][i + 1]["Mesh"],
                json_data[category][i + 1]["Show"] and json_data[category][0]["Show"],
            )


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    # Add the custom icons
    add_custom_icons()

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
