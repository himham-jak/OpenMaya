##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy

from . import export


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


##############################################################################
# Functions
##############################################################################


def fill_template(template, fields):
    with open(template, "r") as f:
        src = string.Template(f.read())
        return src.substitute(fields)


def write_file(file, text):
    with open(file, "w") as f:
        f.write(text)


def update_config():
    script_path = os.path.dirname(__file__)
    custom_levels_path = bpy.context.scene.level_properties.custom_levels_path
    config_fields = {
            "custom_levels_path": custom_levels_path,
        }
    content = fill_template(
        os.path.join(script_path, "templates\\config_template.txt"),
        config_fields,
        )
    write_file(os.path.join(script_path, "userdata\\openmaya_config.json"), content)


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
