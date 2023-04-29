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


# put all of this in json
PAT_MODES = [
  ("ground", "Ground", "", 0),
  ("wall", "Wall", "", 1),
  ("obstacle", "Obstacle", "", 2),
]


PAT_SURFACES = [
  ("stone", "Stone", "", 0),
  ("ice", "Ice", "", 1),
  ("quicksand", "Quicksand", "", 2),
  ("waterbottom", "Water Bottom", "", 3),
  ("tar", "Tar", "", 4),
  ("sand", "Sand", "", 5),
  ("wood", "Wood", "", 6),
  ("grass", "Grass", "", 7),
  ("pcmetal", "PC Metal", "", 8),
  ("snow", "Snow", "", 9),
  ("deepsnow", "Deep Snow", "", 10),
  ("hotcoals", "Hot Coals", "", 11),
  ("lava", "Lava", "", 12),
  ("crwood", "Crate Wood", "", 13),
  ("gravel", "Gravel", "", 14),
  ("dirt", "Dirt", "", 15),
  ("metal", "Metal", "", 16),
  ("straw", "Straw", "", 17),
  ("tube", "Tube", "", 18),
  ("swamp", "Swamp", "", 19),
  ("stopproj", "Stop Proj", "", 20),
  ("rotate", "Rotate", "", 21),
  ("neutral", "Neutral", "", 22),
]


PAT_EVENTS = [
  ("none", "None", "", 0),
  ("deadly", "Deadly", "", 1),
  ("endlessfall", "Endless Fall", "", 2),
  ("burn", "Burn", "", 3),
  ("deadlyup", "Deadly Up", "", 4),
  ("burnup", "Burn Up", "", 5),
  ("melt", "Melt", "", 6),
]


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class GeomProperties(bpy.types.PropertyGroup):

    apply_collision: bpy.props.BoolProperty(
        name="Custom Collision",
        description="Check if you'd like to customize the collision of this face",
        default=False,
    )

    show_invisible: bpy.props.BoolProperty(
        name="Show invisible faces",
        description="Check if you'd like to see invisible faces in the viewport",
        default=True,
    )

    invisible: bpy.props.BoolProperty(
        name="Invisible",
        description="Check to assign the selected faces invisibility",
        default=True,
    )

    invisible_color: bpy.props.FloatVectorProperty(
        name="Viewport Color",
        subtype="COLOR",
        description="Viewport color for invisible faces",
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0
    )

    show_no_edge: bpy.props.BoolProperty(
        name="Show no-edge faces",
        description="Check if you'd like to see no-edge faces in the viewport",
        default=True,
    )

    no_edge: bpy.props.BoolProperty(
        name="No-Edge",
        description="Check to assign the selected faces no edges",
        default=False,
    )

    no_edge_color: bpy.props.FloatVectorProperty(
        name="Viewport Color",  
        subtype="COLOR",
        description="Viewport color for no-edge faces",
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0
    )


classes.append(GeomProperties)  # Add the class to the array


class FaceButtonGroup:

    def __init__(self, name):

        self.name = name

    def draw(self, context, parent):
        row1 = parent.row()
        row2 = parent.row()
        obj = context.object

        row1.prop(
            obj.active_material,
            f"set_{self.name}",
            text=self.name.title(),
            #description=f"Check to assign {self.name} to the selected faces",
            #default=False,
            )

        row2.prop(
            obj.active_material,
            f"show_{self.name}",
            icon="HIDE_OFF",
            icon_only=True,
            #description="Check if you'd like to see invisible faces in the viewport"
            )

        row2.prop(
            obj.active_material,
            f"color_{self.name}",
            text="Viewport Color",
            #subtype="COLOR",
            #description=f"Viewport color for {self.name} faces",
            #default=(1.0, 1.0, 1.0),
            #min=0.0, max=1.0
            )


# Don't add the generic class to the array


class OBJECT_PT_GeomInfoMenu(bpy.types.Panel):
    """"""

    bl_idname = "OBJECT_PT_GeomInfoMenu"
    bl_label = "Geometry Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OpenMaya"
    bl_context = "mesh_edit"

    def draw(self, context):

        layout = self.layout
        geom_properties = context.scene.geom_properties
        obj = context.object

        draw_props(self, context)

classes.append(OBJECT_PT_GeomInfoMenu)  # Add the class to the array


class AddMaterialOperator(bpy.types.Operator):
    """Export the selected options"""  # Be careful, operator docstrings are exposed to the user

    bl_idname = "wm.new_material"  # Unique operator reference name
    bl_label = "+"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    #add poll method to restrict execute with error

    def execute(self, context):  # execute() is called when running the operator

        obj = context.object

        # This line creates a "0" bug in the dropdown ui but I can't fix all of Blender's UI
        #obj.active_material = obj.active_material.copy()

        obj.data.materials.append(obj.active_material.copy())

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(AddMaterialOperator)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


def draw_props(self, context):

    layout = self.layout
    obj = context.object

    # Material chooser
    matrow = layout.row()

    # This needs to work per face, not per object
    matrow.prop(obj, "active_material", text="Selected Material")

    matrow.operator("wm.new_material", icon="ADD", text="")

    # Toggle invisibility
    layout.prop(obj.active_material, "set_invisible")

    # Toggle custom collision
    layout.prop(obj.active_material, "set_collision", icon="TEXT") # change icon
    if (obj.active_material.set_collision):

        # Toggle collision options
        row1 = layout.row()
        row1.prop(obj.active_material, "ignore")
        row1.prop(obj.active_material, "noedge")
        row1.prop(obj.active_material, "noentity")
        row1.prop(obj.active_material, "nolineofsight")
        row2 = layout.row()
        row2.prop(obj.active_material, "nocamera")

        # Collision dropdowns
        layout.prop(obj.active_material, "collide_mode")
        layout.prop(obj.active_material, "collide_surface")
        layout.prop(obj.active_material, "collide_event")


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.Scene.geom_properties = bpy.props.PointerProperty(type=GeomProperties)

    bpy.types.Material.geom_properties = bpy.props.PointerProperty(type=GeomProperties)

    bpy.types.Material.set_invisible = bpy.props.BoolProperty(name="Invisible")
    bpy.types.Material.show_invisible = bpy.props.BoolProperty(name="Show Invisible")
    bpy.types.Material.color_invisible = bpy.props.BoolProperty(name="Viewport Color")

    # Custom collision toggle
    bpy.types.Material.set_collision = bpy.props.BoolProperty(name="Toggle Custom Collision")

    # Custom collision options
    bpy.types.Material.ignore = bpy.props.BoolProperty(name="Ignore")
    bpy.types.Material.noedge = bpy.props.BoolProperty(name="No-Edge")
    bpy.types.Material.noentity = bpy.props.BoolProperty(name="No-Entity")
    bpy.types.Material.nolineofsight = bpy.props.BoolProperty(name="No-LOS")
    bpy.types.Material.nocamera = bpy.props.BoolProperty(name="No-Camera")

    bpy.types.Material.collide_mode = bpy.props.EnumProperty(items = PAT_MODES, name = "Mode")
    bpy.types.Material.collide_surface = bpy.props.EnumProperty(items = PAT_SURFACES, name = "Surface")
    bpy.types.Material.collide_event = bpy.props.EnumProperty(items = PAT_EVENTS, name = "Event")

    # Add the geometry custom properties to the Material Properties tab
    bpy.types.MATERIAL_PT_custom_props.prepend(draw_props)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.geom_properties

    bpy.types.MATERIAL_PT_custom_props.remove(draw_func)

    #del all the extras?


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
