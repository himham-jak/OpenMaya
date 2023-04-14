##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import os
import string
import json

from . import export


##############################################################################
# Constants
##############################################################################


# Path to this script
SCRIPT = os.path.dirname(__file__)


# Relative path to the config file
CONFIG = "userdata\\openmaya_config.json"


# Relative path to the config template
CONFIG_TEMPLATE = "templates\\config_template.txt"


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
    custom_levels_path = bpy.context.scene.level_properties.custom_levels_path
    config_fields = {
            "custom_levels_path": custom_levels_path,
        }
    content = fill_template(
        os.path.join(SCRIPT, CONFIG_TEMPLATE),
        config_fields,
        )
    write_file(os.path.join(SCRIPT, CONFIG), content)


def read_from_config(key):
    with open(os.path.join(SCRIPT, CONFIG), "r") as f:
        return json.loads(f.read())[key]


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
