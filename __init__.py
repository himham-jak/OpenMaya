bl_info = {
    "name": "OpenMaya",
    "description": "Custom level editing tools for the OpenGoal version of the Jak and Daxter series.",
    "author": "himham, evelyntsmg (code), water111 (code), kuitar (graphics)", # TODO: change
    "version": (0, 1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > N Toolbar > Level Info", # TODO: change
    "warning": "Beta Build",
    "doc_url": "https://github.com/himham-jak/OpenMaya", # TODO: change
    "tracker_url": "https://github.com/himham-jak/OpenMaya/issues",
    "support": "COMMUNITY",
    "category": "Development",
}


# TODO: docstring


##############################################################################
# Imports           Order: Imports, Custom Modules
##############################################################################

# Updater ops import, prefs in this file
# TODO move to a new module
from . import addon_updater_ops

# Importing io allows us to debug this file before registration
from . import io

# Not gonna get far without importing bpy
imports = [
    "bpy",
]  # <import_name>


modules = [
    "level_menu",
    "geom_menu",
    "browser",
    "actor_menu",
    "add_actor",
    "export",
    "gizmos",
    "api",
    "io", # Haven't found circular issues importing once for debugging, once for registration
]  # <module_name>.py

# Splash screen
io.debug("OpenMaya Startup\n")
# TODO make splash screen

# Import the imports list
io.debug("Import Start\n")
for imp in imports:
    exec(f"import {imp}")
    io.verbose(f"{imp} import success")
print()

# Import the modules list
io.mods(modules)
print()

##############################################################################
# Constants
##############################################################################


##############################################################################
# Properties and Classes
##############################################################################


@addon_updater_ops.make_annotations
class DemoPreferences(bpy.types.AddonPreferences):
    """Updater Preferences"""

    bl_idname = __package__

    # Addon updater preferences.

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
    )

    updater_interval_months = bpy.props.IntProperty(
        name="Months",
        description="Number of months between checking for updates",
        default=0,
        min=0,
    )

    updater_interval_days = bpy.props.IntProperty(
        name="Days",
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31,
    )

    updater_interval_hours = bpy.props.IntProperty(
        name="Hours",
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23,
    )

    updater_interval_minutes = bpy.props.IntProperty(
        name="Minutes",
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59,
    )

    def draw(self, context):
        layout = self.layout

        # Works best if a column, or even just self.layout.
        mainrow = layout.row()
        col = mainrow.column()

        # Updater draw function, could also pass in col as third arg.
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # ops = col.operator("wm.url_open","Open webpage ")
        # ops.url=addon_updater_ops.updater.website


##############################################################################
# Functions
##############################################################################


# Some functions are intentional repeats which run in context without importing io


def action(verb, item, instruction):
    """Generic Action"""
    try:
        io.verbose(f"{item} {verb} success")
        return exec(instruction)
    except Exception as e:
        io.error("unregister", f"{item}", e)


def reg(item, instruction):
    """Generic Registration"""
    action("register", item, instruction)


def reg_mod(item):
    """Module Registration"""
    reg(item, f"{item}.register()")


def reg_cls(item):
    """Class Registration"""
    reg(item, f"bpy.utils.register_class({item})")


def unreg(item, instruction):
    """Generic Unregistration"""
    action("unregister", item, instruction)


def unreg_mod(item):
    """Module Unregistration"""
    unreg(item, f"{item}.unregister()")


def unreg_cls(item):
    """Class Unregistration"""
    unreg(item, f"bpy.utils.unregister_class({item})")


##############################################################################
# Registration
##############################################################################


def register():

    io.verbose("Registration Start\n")

    # Register all classes
    reg_cls("DemoPreferences")

    # Registering this one first, bl_info isn't passed to any other module
    addon_updater_ops.register(bl_info)

    # Register all modules
    for module in modules:
        reg_mod(module)


def unregister():

    # Unregister all modules, including the stray
    for module in reversed(["addon_updater_ops"]+modules):
        unreg_mod(module)

    # Unregister all classes
    unreg_cls("DemoPreferences")


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
