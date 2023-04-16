##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import typing
import re
import os
import json
import colorsys
import bmesh

from . import export
from . import config_controller


##############################################################################
# Constants
##############################################################################


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class GeomProperties(bpy.types.PropertyGroup):

    face_name: bpy.props.StringProperty(
        name="Face Name",
        description="",
        default="face1",
        maxlen=1024,
    )

    invisible: bpy.props.BoolProperty(
        name="Invisible",
        description="Check if you'd like the level info to be included when you export",
        default=True,
    )

    invisible_color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype="COLOR",
        description="",
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0
    )

    apply_collision: bpy.props.BoolProperty(
        name="Level Info",
        description="",
        default=False,
    )

    no_edge: bpy.props.BoolProperty(
        name="No Edge",
        description="",
        default=False,
    )


classes.append(GeomProperties)  # Add the class to the array


class OBJECT_PT_GeomInfoMenu(bpy.types.Panel):
    """"""

    bl_idname = "OBJECT_PT_LevelInfoMenu"
    bl_label = "Geometry Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level Editor"
    bl_context = "objectmode"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        geom_properties = scene.geom_properties

        def input_invalid(chars, value):
            return not (bool(re.match(chars, value)) and value)

        # set these properties manually
        layout.prop(geom_properties, "face_name", icon="TEXT")

        title = layout.row()

        title.prop(geom_properties, "apply_collision", icon="HIDE_OFF", icon_only=True)

        title.prop(geom_properties, "invisible")
        title.prop(geom_properties, "invisible_color")


classes.append(OBJECT_PT_GeomInfoMenu)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.Scene.geom_properties = bpy.props.PointerProperty(type=GeomProperties)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.geom_properties


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
