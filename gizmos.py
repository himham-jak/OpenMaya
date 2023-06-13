# TODO: docstring


##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
from bpy.types import GizmoGroup
from bpy_extras import view3d_utils


##############################################################################
# Constants
##############################################################################


##############################################################################
# Properties and Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class GizmoProperties(bpy.types.PropertyGroup):

    show_contents: bpy.props.BoolProperty(
        name="Contents",
        description="Gizmo to show the contents of a crate, etc",
        default=True,
    )


classes.append(GizmoProperties)  # Add the class to the array


class ActorGizmos(GizmoGroup):
    """"""

    bl_idname = "OBJECT_GGT_custom_gizmo"
    bl_label = "Custom Gizmo"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"
    bl_options = {"PERSISTENT", "SCALE"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object

        # Only show a gizmo if an actor is currently selected
        return obj.select_get() and ("Actor Type" in obj.keys())

    def draw_prepare(self, context):
        obj = context.active_object

        # Grab the 2D position of the object in viewport
        view3d_position = view3d_utils.location_3d_to_region_2d(
            bpy.context.region,
            bpy.context.space_data.region_3d,
            obj.location,
            default=None,
        )

        # Move the gizmo to the x,y coordinates
        self.foo_gizmo.matrix_basis[0][3] = view3d_position[0]
        self.foo_gizmo.matrix_basis[1][3] = view3d_position[1]

    def setup(self, context):
        obj = context.active_object

        giz = self.gizmos.new("GIZMO_GT_button_2d")

        # TODO Custom icons
        giz.icon = "CANCEL"

        self.foo_gizmo = giz


classes.append(ActorGizmos)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


def add_custom_gizmo_bools(self, context):

    layout = self.layout
    scene = context.scene
    gizmo_properties = scene.gizmo_properties

    layout.label(text="Actors")
    layout.prop(gizmo_properties, "show_contents")


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.Scene.gizmo_properties = bpy.props.PointerProperty(type=GizmoProperties)

    # Add the custom gizmo booleans to the gizmo menu
    bpy.types.VIEW3D_PT_gizmo_display.append(add_custom_gizmo_bools)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.gizmo_properties


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
