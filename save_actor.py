# TODO: docstring


##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import os
import string


##############################################################################
# Constants
##############################################################################


##############################################################################
# Properties and Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class SaveActorOperator(bpy.types.Operator):
    """Saves the current actor to the "saved" subfolder of the "add actor" menu"""

    bl_idname = "wm.save_actor"  # Unique operator reference name
    bl_label = "Save Preset"  # String for the UI
    bl_options = {"REGISTER"}  # Enable undo for the operator

    def execute(self, context):  # execute() is called when running the operator

        # Grab the selected actor
        actor = context.active_object

        # Fields to fill in the template files
        actor_fields = {
            "actor_name": actor.name,
            "actor_etype": actor["Actor Type"],
            "actor_game_task": actor["Game Task"],
            "actor_mesh_name": actor["Mesh"],
            "actor_icon_name": actor["Icon"],
        }

        # Path to this script
        script_path = os.path.dirname(__file__)

        def fill_template(template, fields):
            with open(template, "r") as f:
                src = string.Template(f.read())
                return src.substitute(fields)

        def insert_before(file, text, divider):
            with open(file, "r") as f:
                contents = f.readlines()

            with open(file, "w") as f:
                for line in contents:
                    # This is a shitty implementation
                    if divider in line:
                        f.write(text)
                    f.write(line)

        # Export the normal properties
        content = fill_template(
            os.path.join(script_path, "templates\\saved_actor_template.txt"),
            actor_fields,
        )

        insert_before(
            os.path.join(script_path, f"saved_actors.json"),
            content,
            "]",
        )

        for key, value in actor.items():
            if key in [
                "Actor Type",
                "Game Task",
                "Mesh",
                "Icon",
                "JSON Category",
                "JSON Index",
            ]:
                continue
            print(f"{key} : {value}")

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(SaveActorOperator)  # Add the class to the array


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
