##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


imports = [
    "bpy",
    "os",
    "time",
]  # <module_name>.py


import bpy
import os
import time


##############################################################################
# Constants
##############################################################################

# Path to this script
SCRIPT = os.path.dirname(__file__)

# Name of this script
NAME = os.path.basename(__file__)[0]


# Relative path to the config file
CONFIG = "userdata\\openmaya_config.json"


# Relative path to the config template
CONFIG_TEMPLATE = "templates\\config_template.txt"


# Error string for config loading
CONFIG_ERROR = "Unable to load {} from config"


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


##############################################################################
# Functions
##############################################################################


def log(source, message):
    """Generic Logging"""
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"{current_time} - [{source}] : {message}")


def debug(message):
    """Debug Logging"""
    log("DEBUG", message)


def verbose(message):
    """Verbose Logging"""
    log("VERBOSE", message)


def error(verb, item, e):
    """Generic Error"""
    debug(f"Error {verb}ing {item}:")
    debug(f"{e}")
    return "E"


def reg_error(item, e):
    """Registration Error"""
    error("register", f"{item}", e)


def unreg_error(item, e):
    """UnRegistration Error"""
    error("unregister", f"{item}", e)


def fill_template(template, fields):
    with open(template, "r") as f:
        src = string.Template(f.read())
        return src.substitute(fields)


def write_file(file, text):
    with open(file, "w") as f:
        f.write(text)


def write_config(): # Add try, except
    custom_levels_path = bpy.context.scene.level_properties.custom_levels_path
    config_fields = {
            "custom_levels_path": custom_levels_path,
        }
    content = fill_template(
        os.path.join(SCRIPT, CONFIG_TEMPLATE),
        config_fields,
        )
    write_file(os.path.join(SCRIPT, CONFIG), content)


def read_config(key):
    """Return the value from config"""
    try:
        with open(os.path.join(SCRIPT, CONFIG), "r") as f:
            return json.loads(f.read())[key]
    except (Exception) as e: # Catch the errors
        return  error("read", key, e)


def action(verb, item, instruction):
    """Generic Action"""
    try:
        verbose(f"\t{item} {verb} success")
        return exec(instruction)
    except Exception as e:
        reg_error(item, e)


def batch(verb, items, instruction):
    """Generic batch pattern"""
    for item in items:
        action(verb, item, instruction.format(item))


def imp(item):
    """Import"""
    action("import", item, f"import {item}")


def imps(items):
    """Batch Import"""
    batch("import", items, "import {}")


def mod(item):
    """Module Import"""
    action("import", item, f"from . import {item}")


def mods(items):
    """Batch Module Import"""
    batch("import", items, "from . import {}")


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        verbose(f"{NAME}.{cls} class registered")
        bpy.utils.register_class(cls)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        verbose(f"{NAME}.{cls} class unregistered")
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
