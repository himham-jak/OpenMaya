##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import re


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

    anchor: bpy.props.StringProperty(
        name="Anchor",
        description="The Parent of all your level geometry. The anchor itself will not export.\nSuggestion: Create a new empty, Parent all your geometry to it. Select the empty here.",
        maxlen=1024,
    )

    spawn_location: bpy.props.FloatVectorProperty(
        name="Spawn Location",
        description="The location in 3d space to place Jak.\nDefault: 0,0,0",
        default=(0.0, 0.0, 0.0),
    )

    level_rotation: bpy.props.FloatVectorProperty(
        name="Level Rotation",
        description="The quaternion rotation in 3d space to place your custom level.\nDefault: 0,0,0,1",
        default=(0.0, 0.0, 0.0),  # Blender doesn't want me to make a 4d vector
        min=0.0,
        max=1.0,
    )

    custom_levels_path: bpy.props.StringProperty(
        name="Working Directory",
        description="The path to /custom_levels/ in the OpenGOAL distribution",
        # default=json_data["Custom Levels Path"],
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


classes.append(LevelProperties)  # Add the class to the array


class OBJECT_PT_LevelInfoMenu(bpy.types.Panel):
    """"""

    bl_idname = "OBJECT_PT_LevelInfoMenu"
    bl_label = "Level Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level Editor"
    bl_context = "objectmode"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        level_properties = scene.level_properties

        def input_valid(chars, value):
            return not (bool(re.match(chars, value)) and value)

        # set these properties manually
        title = layout.row()
        title.alert = input_valid("^[A-Za-z-]*$", level_properties.level_title)
        title.prop(level_properties, "level_title", icon="TEXT")

        nick = layout.row()
        nick.alert = input_valid("^[A-Za-z]*$", level_properties.level_nickname)
        nick.prop(level_properties, "level_nickname", icon="TEXT")

        anch = layout.row()
        anch.prop_search(
            level_properties, "anchor", scene, "objects", icon="EMPTY_AXIS"
        )

        layout.prop(level_properties, "spawn_location", text="Spawn Location*")

        # layout.prop(bpy.context.scene.objects[level_properties.anchor], "location", text="Anchor Location*")

        layout.prop(level_properties, "level_rotation", text="Level Rotation*")

        # layout.operator("wm.create_world_reference")

        layout.prop(level_properties, "custom_levels_path")

        layout.prop(level_properties, "should_export_level_info")

        layout.prop(level_properties, "should_export_actor_info", text="Actor Info*")

        layout.prop(level_properties, "should_export_geometry")

        layout.prop(level_properties, "should_playtest_level")

        # layout.operator("wm.export")

        layout.label(
            text="Options with * do not currently export/function.", icon="ERROR"
        )

        layout.separator()


classes.append(OBJECT_PT_LevelInfoMenu)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


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
