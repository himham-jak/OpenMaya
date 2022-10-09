##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import os
import string


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class ExportOperator(bpy.types.Operator):
    """Move all objects in the scene by one unit in the x direction."""

    bl_idname = "wm.export"  # Unique operator reference name
    bl_label = "Export"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    def execute(self, context):  # execute() is called when running the operator

        # Grab the level properties from the level menu
        props = context.scene.level_properties

        # Grab the working directory
        working_dir = props.custom_levels_path

        # Validate the above info

        # Path to this script
        script_path = os.path.dirname(__file__)

        # Path to level
        level_path = os.path.join(working_dir, props.level_title)
        # If it doesn't exist, make it
        if not os.path.exists(level_path):
            os.mkdir(level_path)

        # Path to game.gp
        game_path = os.path.join(
            os.path.dirname(os.path.dirname(working_dir)), "goal_src\\jak1"
        )

        # Path to level-info.gc
        level_info_path = os.path.join(
            os.path.dirname(os.path.dirname(working_dir)),
            "goal_src\\jak1\\engine\\level",
        )

        # Level title with no dash
        leveltitle = props.level_title.replace("-", "")

        # Fields to fill in the template files
        fields = {
            "level_title": props.level_title,
            "leveltitle": leveltitle,
            "level_nickname": props.level_nickname.lower(),
            "level_NICKNAME": props.level_nickname.upper(),
        }

        def fill_template(template, fields):
            with open(template, "r") as f:
                src = string.Template(f.read())
                return src.substitute(fields)

        def write_file(file, text):
            with open(file, "w") as f:
                f.write(text)

        def append_file(file, text):
            with open(file, "a") as f:
                f.write(text)

        # Check if the user wants to export level info
        if props.should_export_level_info:

            # leveltitle.gd
            content = fill_template(
                os.path.join(script_path, "leveltitle_gd_template.txt"), fields
            )
            write_file(os.path.join(level_path, f"{leveltitle}.gd"), content)

            # ../goal_src/jak1/game.gp
            content = fill_template(
                os.path.join(script_path, "game_gp_template.txt"), fields
            )
            append_file(os.path.join(game_path, "game.gp"), content)

            # ../goal_src/jak1/engine/level/level-info.gc
            content = fill_template(
                os.path.join(script_path, "level-info_gc_template.txt"), fields
            )
            append_file(os.path.join(level_info_path, "level-info.gc"), content)

            print(props.anchor)
            print(props.spawn_location[0])
            print(props.level_rotation)

        # Check if there is a collection of actors and if the user wants to export them
        if (
            "Actor Collection" in bpy.data.collections
        ) and props.should_export_actor_info:
            actors = bpy.data.collections["Actor Collection"].objects

            # Iterate through the actors and export the actor info
            for actor in actors:

                # Export the normal properties
                print(actor.name)
                print(actor.location)
                print(actor.rotation_quaternion)

                # Export the custom properties
                for key, value in actor.items():
                    print(f"{key}:{value}")

        # Check if the user wants to export the geometry
        if props.should_export_geometry:

            # Deselect everything
            bpy.ops.object.select_all(action="DESELECT")

            # Select everything but the actors
            for obj in bpy.data.objects:
                obj.select_set("Actor Type" not in obj.keys())

            # level-title.glb
            bpy.ops.export_scene.gltf(
                filepath=os.path.join(level_path, f"{props.level_title}.glb"),
                use_selection=True,  # export only the selection
            )

        # Check if the user wants to playtest
        if props.should_playtest_level:

            # Do that
            print("playtest")

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(ExportOperator)  # Add the class to the array


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
