##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
from bpy.types import GizmoGroup
from bpy_extras import view3d_utils
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
import os


##############################################################################
# Classes
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
        # Get currently selected object
        obj = context.active_object

        # Grab the 2D position of the object in viewport
        view3d_position = view3d_utils.location_3d_to_region_2d(
            bpy.context.region,
            bpy.context.space_data.region_3d,
            obj.location,
            default=None,
        )

        # Create a 2d gizmo
        giz = self.gizmos.new("GIZMO_GT_button_2d")

        # Where the icon would have gone
        # giz.icon = "BLANK1"
        giz.icon = "CANCEL"
        # Nothing between these lines or everything breaks
        self.foo_gizmo = giz

        self.pseudo_icon = setup_pseudo_icon(view3d_position, 30, 30)

        # TODO Not sure when to run this
        # Kills the pseudo icon
        # bpy.types.SpaceView3D.draw_handler_remove(draw,"WINDOW")


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


def setup_pseudo_icon(position, width, height):

    gpu.state.blend_set("ALPHA")

    # Path to the folder where the icon is
    # The path is calculated relative to this py file inside the addon folder
    my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # Find the icon image
    img_filepath = os.path.join(my_icons_dir, "babak.png")

    # Need to supply a "bpy.types.image" to the draw handler
    img = bpy.data.images.load(img_filepath)

    # Make the image into a texture
    texture = gpu.texture.from_image(img)

    # Make shader
    shader = gpu.shader.from_builtin("2D_IMAGE")

    # Supply the coordinates
    batch = batch_for_shader(
        shader,
        "TRI_FAN",
        {
            "pos": (
                (position[0] - width / 2, position[1] - height / 2),
                (position[0] + width / 2, position[1] - height / 2),
                (position[0] + width / 2, position[1] + height / 2),
                (position[0] - width / 2, position[1] + height / 2),
            ),
            "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
        },
    )

    # Full function to pass to the draw handler
    def draw():
        obj = bpy.context.active_object

        # Grab the 2D position of the object in viewport
        position = view3d_utils.location_3d_to_region_2d(
            bpy.context.region,
            bpy.context.space_data.region_3d,
            obj.location,
            default=None,
        )
        batch = batch_for_shader(
            shader,
            "TRI_FAN",
            {
                "pos": (
                    (position[0] - width / 2, position[1] - height / 2),
                    (position[0] + width / 2, position[1] - height / 2),
                    (position[0] + width / 2, position[1] + height / 2),
                    (position[0] - width / 2, position[1] + height / 2),
                ),
                "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
            },
        )
        shader.bind()
        shader.uniform_sampler("image", texture)
        batch.draw(shader)

    # Create the pseudo-icon
    return bpy.types.SpaceView3D.draw_handler_add(draw, (), "WINDOW", "POST_PIXEL")


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.Scene.gizmo_properties = bpy.props.PointerProperty(type=GizmoProperties)

    # Add the custom gizmo booleans to the gizmo menu
    # TODO unregister
    bpy.types.VIEW3D_PT_gizmo_display.append(add_custom_gizmo_bools)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.gizmo_properties


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
