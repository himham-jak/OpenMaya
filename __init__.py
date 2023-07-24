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
    "ui",
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


MENU_LOC = [
  ("n", "N Toolbar", "", 0),
  ("prop", "Properties Editor", "", 1),
  ("hide", "Hide", "", 2),
]


ADD_MENU_LOC = [
  ("mesh", "Mesh", "", 0),
  ("sub", "Mesh > Actors", "", 1),
  ("actors", "Actors", "", 2),
  ("hide", "Hide", "TEXT", 3),
]


ACTOR_DETAIL = [
  ("all", "Extensive", "", 0),
  ("min", "Minimal", "", 1),
]


##############################################################################
# Properties and Classes
##############################################################################


@addon_updater_ops.make_annotations
class UserPreferences(bpy.types.AddonPreferences):
    """Tip: Place global preferences here and pull them out with:
                settings = get_user_preferences(context)
                settings.auto_check_update
        Like: whether or not to render a panel."""

    bl_idname = __package__

    # Install preferences

    # dir/nickname dropdown
    
    allow_sockets: bpy.props.BoolProperty(
        name="Allow the use of sockets.",
        description="Check if you'd like to allow the use of sockets",
        default=True,
    )
    
    # auto edit/ml
    auto_compile: bpy.props.BoolProperty(
        name="Automatically compile file changes",
        description="Check if you'd like to automatically compile file changes",
        default=True,
    )
    
    # auto clear command stack
    auto_send: bpy.props.BoolProperty(
        name="Automatically send any DECI2 packets on the stack",
        description="Check if you'd like to automatically send commands to a REPL",
        default=True,
    )

    # import models from game
    rip_models: bpy.props.BoolProperty(
        name="Import geometry and actor models from the game",
        description="Check if you'd like your actors to look real and your levels to fit in seamlessly",
        default=True,
    )

    # auto run REPL and GK for patch
    auto_patch: bpy.props.BoolProperty(
        name="Don't ask before opening a REPL or game while patching",
        description="Uncheck if you'd like to always be asked",
        default=True,
    )
    
    # Geometry preferences
    
    # File preferences

    level_menu_loc: bpy.props.EnumProperty(
        name="Level Menu Location",
        items=MENU_LOC,
        description="Choose what panel the Level Info tab calls home",
        default=0,
    )

    show_level_menu_icons: bpy.props.BoolProperty(
        name="Show Icons",
        description="Check if you'd like to see icons in the Level Info panel",
        default=True,
    )
    
    # Playtesting preferences

    # Actor Preferences

    actor_menu_loc: bpy.props.EnumProperty(
        name="Actor Menu Location",
        items=MENU_LOC,
        description="Choose what panel the Actor Info tab calls home",
        default=0,
    )

    actor_menu_detail: bpy.props.EnumProperty(
        name="Actor Menu Detail",
        items=ACTOR_DETAIL,
        description="Choose the level of detail for your actor editing preferences",
        default=0,
    )

    add_menu_loc: bpy.props.EnumProperty(
        name="Add Menu Location",
        items=ADD_MENU_LOC,
        description="Choose what dropdown the Add Actor tab calls home",
        default=0,
    )

    show_actor_menu_icons: bpy.props.BoolProperty(
        name="Show Icons",
        description="Check if you'd like to see icons in the Actor Info panel",
        default=True,
    )

    show_add_menu_icons: bpy.props.BoolProperty(
        name="Show Icons",
        description="Check if you'd like to see icons in the Add Actor dropdown",
        default=True,
    )

    show_categories: bpy.props.BoolProperty(
        name="Show Categories",
        description="Check if you'd like the actors divided into categories",
        default=True,
    )

    show_sort: bpy.props.BoolProperty(
        name="Show Sort Operators",
        description="Check if you'd like to have sort buttons for the actors",
        default=True,
    )
    
    # Dev preferences

    debug: bpy.props.BoolProperty(
        name="Debug Logging",
        description="Check if you'd like to see debug messages in the console",
        default=False,
    )

    verbose: bpy.props.BoolProperty(
        name="Verbose Logging",
        description="Check if you'd like to see an obnoxious amount of debug messages in the console",
        default=False,
    )

    show_contributions: bpy.props.BoolProperty(
        name="Show Opportunities to Contribute",
        description="Check if you'd like to see inactive features that you could help finish",
        default=False,
    )

    # Updater preferences

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


##############################################################################
# Functions
##############################################################################


# Some functions are intentional repeats which must run without importing io


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
    reg_cls("UserPreferences")

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
    unreg_cls("UserPreferences")


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
