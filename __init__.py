bl_info = {
    "name": "OpenMaya",
    "description": "Custom level editing tools for the OpenGoal version of the Jak and Daxter series.",
    "author": "himham, water111 (integrated code), kuitar (new graphics)",
    "version": (0, 0, 2),
    "blender": (3, 3, 0),
    "location": "View3D > N Toolbar > Level Info",
    "warning": "Alpha Build",
    "doc_url": "https://github.com/himham-jak/OpenMaya",
    "tracker_url": "https://github.com/himham-jak/OpenMaya/issues",
    "support": "COMMUNITY",
    "category": "Development",
}


import bpy


# Updater ops import, all setup in this file.
from . import addon_updater_ops


modules = [
    "level_menu",
    "geom_menu",
    "actor_menu",
    "add_actor",
    "export",
    "gizmos",
]  # <module_name>.py


##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


for module in modules:  # Import all modules listed in the modules array
    try:
        exec(f"from . import {module}")
    except Exception as e:
        print(f"Error importing {module}.py")
        print(e)


##############################################################################
# Preferences
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
# Registration
##############################################################################


def register():

    addon_updater_ops.register(bl_info)

    bpy.utils.register_class(DemoPreferences)

    for module in modules:  # Register all the modules
        try:
            exec(f"{module}.register()")
        except Exception as e:
            print(f"Error registering {module}.py")
            print(e)


def unregister():

    for module in reversed(modules):  # Unregister all the modules
        try:
            exec(f"{module}.unregister()")
        except Exception as e:
            print(f"Error unregistering {module}.py")
            print(e)

    bpy.utils.unregister_class(DemoPreferences)

    addon_updater_ops.unregister()


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
