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
    """Export the selected options"""  # Be careful, operator docstrings are exposed to the user

    bl_idname = "wm.export"  # Unique operator reference name
    bl_label = "Export"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    def execute(self, context):  # execute() is called when running the operator

        # Grab the level properties from the level menu
        props = context.scene.level_properties

        # Grab the working directory
        working_dir = props.custom_levels_path

        # Validate the above info

        # Save the blend file
        bpy.ops.wm.save_as_mainfile(
            filepath=os.path.join(working_dir, f"{props.level_title}.blend")
        )

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

        def bool_to_string(cond):
            if cond:
                return "true"
            return "false"

        # Fields to fill in the template files
        level_fields = {
            "level_title": props.level_title,
            "leveltitle": leveltitle,
            "LEVELTITLE": leveltitle.upper(),
            "level_nickname": props.level_nickname.lower(),
            "level_NICKNAME": props.level_nickname.upper(),
            "automatic_wall_detection": bool_to_string(props.automatic_wall_detection),
            "automatic_wall_angle": props.automatic_wall_angle,
            "double_sided_collide": bool_to_string(props.double_sided_collide),
        }

        def fill_template(template, fields):
            with open(template, "r") as f:
                src = string.Template(f.read())
                return src.substitute(fields)

        def write_file(file, text):
            with open(file, "w") as f:
                f.write(text)

        def insert_after(file, text, divider):
            with open(file, "r") as f:
                contents = f.readlines()

            with open(file, "w") as f:
                for line in contents:
                    f.write(line)
                    # This is a shitty implementation
                    if divider in line:
                        f.write(text)

        def append_file(file, text):
            with open(file, "a") as f:
                f.write(text)

        def backup_file(file, backup):
            with open(file, "r") as f:
                contents = f.readlines()

            with open(backup, "w") as f:
                for line in contents:
                    f.write(line)

        # Check if the user wants to export level info
        if props.should_export_level_info:

            # ./leveltitle.gd
            content = fill_template(
                os.path.join(script_path, "templates\\leveltitle_gd_template.txt"),
                level_fields,
            )
            write_file(os.path.join(level_path, f"{leveltitle}.gd"), content)

            # ../goal_src/jak1/game.gp
            content = fill_template(
                os.path.join(script_path, "templates\\game_gp_template.txt"),
                level_fields,
            )

            backup_file(
                os.path.join(game_path, "game.gp"),
                os.path.join(game_path, "game.bak"),
            )

            insert_after(
                os.path.join(game_path, "game.gp"),
                content,
                ";; it should point to the .jsonc file that specifies the level.\n",
            )

            # ../goal_src/jak1/engine/level/level-info.gc
            content = fill_template(
                os.path.join(script_path, "templates\\level-info_gc_template.txt"),
                level_fields,
            )

            backup_file(
                os.path.join(level_info_path, "level-info.gc"),
                os.path.join(level_info_path, "level-info.bak"),
            )

            append_file(os.path.join(level_info_path, "level-info.gc"), content)

            # ./level-title.jsonc
            content = fill_template(
                os.path.join(script_path, "templates\\level-title_jsonc_template.txt"),
                level_fields,
            )

            write_file(os.path.join(level_path, f"{props.level_title}.jsonc"), content)

        # Check if there is a collection of actors and if the user wants to export them
        if (
            "Actor Collection" in bpy.data.collections
        ) and props.should_export_actor_info:
            actors = bpy.data.collections["Actor Collection"].objects

            add_comma = False

            # Iterate through the actors and export the actor info
            for actor in actors:

                # Fields to fill in the template file
                actor_fields = {
                    "actor_name": actor.name,
                    "actor_translation_x": actor.location[0],
                    "actor_translation_y": -actor.location[1],
                    "actor_translation_z": actor.location[2],
                    "actor_quaternion_w": actor.rotation_quaternion[0],
                    "actor_quaternion_x": actor.rotation_quaternion[1],
                    "actor_quaternion_y": actor.rotation_quaternion[2],
                    "actor_quaternion_z": actor.rotation_quaternion[3],
                    "actor_etype": actor["Actor Type"],
                    "actor_game_task": actor["Game Task"],
                }

                # Export the normal properties
                content = fill_template(
                    os.path.join(script_path, "templates\\jsonc_actor_template.txt"),
                    actor_fields,
                )

                if add_comma:
                    content += ",\n"
                else:
                    content += "\n"

                add_comma = True

                insert_after(
                    os.path.join(level_path, f"{props.level_title}.jsonc"),
                    content,
                    '"actors"',
                )

                add_comma = False

                # Export the custom properties
                for key, value in actor.items():

                    # Skip some properties that are irrelevant or already exported
                    if key in [
                        "Actor Type",
                        "Game Task",
                        "Mesh",
                        "Icon",
                        "JSON Category",
                        "JSON Index",
                    ]:
                        continue

                    custom_fields = {
                        "key": key,
                        "value": value,
                    }
                    content = fill_template(
                        os.path.join(
                            script_path, "templates\\jsonc_cust_prop_template.txt"
                        ),
                        custom_fields,
                    )

                    if add_comma:
                        content += ","
                    else:
                        content += "\n"

                    add_comma = True

                    insert_after(
                        os.path.join(level_path, f"{props.level_title}.jsonc"),
                        content,
                        f'"name":"{actor.name}"',
                    )

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
