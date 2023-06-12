bl_info = {
    "name": "OpenMaya",
    "description": "Custom level editing tools for the OpenGoal version of the Jak and Daxter series.",
    "author": "himham, evelyntsmg (code), water111 (code), kuitar (graphics)",
    "version": (0, 1, 0),
    "blender": (3, 3, 0),
    "location": "View3D > N Toolbar > Level Info",
    "warning": "Beta Build",
    "doc_url": "https://github.com/himham-jak/OpenMaya",
    "tracker_url": "https://github.com/himham-jak/OpenMaya/issues",
    "support": "COMMUNITY",
    "category": "Development",
}


##############################################################################
# Imports           Order: Imports, Custom Modules
##############################################################################

from . import addon_updater_ops     # Updater ops import, prefs in this file, move to a module
from . import io                    # Importing io lets us debug this file

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
    "io", # Haven't found any circular issues being imported twice, once for debugging, once for registration
]  # <module_name>.py


io.debug("OpenMaya Startup\n")


io.debug("Import Start\n")


for imp in imports:
    exec(f"import {imp}")
    io.verbose(f"{imp} import success")
print()


io.mods(modules)
print()


##############################################################################
# Preferences and Classes
##############################################################################


@addon_updater_ops.make_annotations
class DemoPreferences(bpy.types.AddonPreferences):
    """Demo bare-bones preferences"""

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

    # Registering this one first, bl_info isn't passedto any other module
    addon_updater_ops.register(bl_info)

    # Register all modules
    for module in modules:  # Register all the modules
        reg_mod(module)


def unregister():

    # Unregister all modules
    for module in reversed(["addon_updater_ops"]+modules):  # Unregister all the modules
        unreg_mod(module)

    # Unregister any classes
    unreg_cls("DemoPreferences")


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
