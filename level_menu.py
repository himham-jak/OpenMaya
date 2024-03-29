##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import typing
import re
import os
import json

from . import export
from . import config_controller


##############################################################################
# Constants
##############################################################################

# Path read out of the json config
CUSTLVL = config_controller.read_from_config("Working Directory")


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class LevelProperties(bpy.types.PropertyGroup):

    level_title: bpy.props.StringProperty(
        name="Level Title",
        description="The name of your custom level.\nOnly letters and dashes are allowed, case will be ignored.\nDefault: my-level",
        default="my-level",
        maxlen=1024,
    )

    level_nickname: bpy.props.StringProperty(
        name="Level Nickname",
        description="The nickname of your custom level.\nThree letters, case will be ignored.\nDefault: lvl",
        default="lvl",
        maxlen=3,
    )

    custom_levels_path: bpy.props.StringProperty(
        name="Working Directory",
        description="The path to \\custom_levels\\ in the OpenGOAL distribution",
        default="",
        maxlen=1024,
        subtype="DIR_PATH",
    )

    should_export_level_info: bpy.props.BoolProperty(
        name="Level Info",
        description="Check if you'd like the level info to be included when you export",
        default=True,
    )

    should_export_actor_info: bpy.props.BoolProperty(
        name="Actor Info",
        description="Check if you'd like the actor info to be included when you export",
        default=True,
    )

    should_export_geometry: bpy.props.BoolProperty(
        name="Level Geometry",
        description="Check if you'd like the level geometry to be included when you export",
        default=True,
    )

    should_playtest_level: bpy.props.BoolProperty(
        name="Playtest Level",
        description="Check if you'd like to launch the level immediately after export",
        default=True,
    )

    automatic_wall_detection: bpy.props.BoolProperty(
        name="Auto Wall Detection",
        description="Check if you'd like the level to automatically create walls above a certain angle",
        default=True,
    )

    automatic_wall_angle: bpy.props.FloatProperty(
        name="Auto Wall Angle",
        description="The angle you'd like the level to automatically create walls above",
        min=0.0,
        max=90.0,
        default=45.0,
    )

    double_sided_collide: bpy.props.BoolProperty(
        name="Double Sided Collision",
        description="Check if you'd like to make all collision mesh triangles double sided",
        default=False,
    )


classes.append(LevelProperties)  # Add the class to the array


class OBJECT_PT_LevelInfoMenu(bpy.types.Panel):
    """"""

    bl_idname = "OBJECT_PT_LevelInfoMenu"
    bl_label = "Level Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level Editor"
    bl_context = "objectmode"

    #@classmethod
    #def poll(self, context):
    #    should_update_config = True
    #    return should_update_config

    def __init__(self):

        props = bpy.context.scene.level_properties
        custom_levels_path = props.custom_levels_path

        # If custom_levels_path is set to empty, immediately replace it with the config default value
        if len(custom_levels_path) < 1:

            try: # Try to update the config settings from the json
                props.custom_levels_path = CUSTLVL

            except Exception as e: # Catch the errors
                print(f"Unable to load values from config\nError: {e}")

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        level_properties = scene.level_properties



        def input_invalid(chars, value):
            return not (bool(re.match(chars, value)) and value)

        # set these properties manually
        title = layout.row()
        title.alert = input_invalid("^[A-Za-z-]*$", level_properties.level_title)

        title.prop(level_properties, "level_title", icon="TEXT")

        nick = layout.row()
        nick.alert = input_invalid("^[A-Za-z]*$", level_properties.level_nickname)
        nick.prop(level_properties, "level_nickname", icon="TEXT")

        # layout.operator("wm.create_world_reference")

        layout.prop(level_properties, "custom_levels_path")

        layout.prop(level_properties, "double_sided_collide")

        layout.prop(level_properties, "automatic_wall_detection")

        layout.prop(level_properties, "automatic_wall_angle")

        layout.separator()

        layout.operator("wm.export")

        layout.prop(level_properties, "should_export_level_info")

        layout.prop(level_properties, "should_export_actor_info")

        layout.prop(level_properties, "should_export_geometry")

        # layout.prop(level_properties, "should_playtest_level")


classes.append(OBJECT_PT_LevelInfoMenu)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


# Need to implement a singleton pattern so this only shows once per error
def show_message(message, title="Message", icon="INFO"):
    """Make a little popup"""

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.Scene.level_properties = bpy.props.PointerProperty(type=LevelProperties)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.level_properties


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
