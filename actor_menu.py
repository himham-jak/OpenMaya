##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class ActorProperties(bpy.types.PropertyGroup):

    actor_name: bpy.props.StringProperty(
        name="Actor Name",
        description="The name of your object (actor).\nOnly lowercase letters and dashes are allowed.\nDefault: my-level",
        default="my-actor",
        maxlen=1024,
    )

    actor_type: bpy.props.StringProperty(
        name="Actor Type",
        description="The etype of the actor",
    )

    actor_translation: bpy.props.FloatVectorProperty(
        name="Actor Translation",
        description="The location in 3d space to place your object (actor).\nDefault: -21.6238,20.0496,17.1191",
        default=(-21.6238, 20.0496, 17.1191),
        min=0.0,
        max=25.0,
    )

    actor_quaternion: bpy.props.FloatVectorProperty(
        name="Actor Quaternion",
        description="The quaternion rotation in 3d space to place your object (actor.\nDefault: 0,0,0,1",
        default=(0.0, 0.0, 0.0),  # Blender doesn't want me to make a 4d vector
        min=0.0,
        max=1.0,
    )


classes.append(ActorProperties)  # Add the class to the array


class OBJECT_PT_ActorInfoMenu(bpy.types.Panel):
    """"""

    bl_idname = "OBJECT_PT_ActorInfoMenu"
    bl_label = "Actor Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level Editor"
    bl_context = "objectmode"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        actor_properties = scene.actor_properties

        layout.prop(context.active_object, "name", text="Actor Name")

        # These properties auto populate

        etype = layout.row()
        etype.enabled = False

        def custom_prop(name, parent=layout):

            if bpy.data.objects[bpy.context.object.data.name].get(name) is not None:
                parent.prop(
                    bpy.data.objects[bpy.context.object.data.name], f'["{name}"]'
                )

        custom_prop("Actor Type", etype)

        layout.prop(context.active_object, "location", text="Actor Translation")

        # This won't display properly unless the object is in quaternion mode, so I force all actors into quat mode when added
        layout.prop(
            context.active_object, "rotation_quaternion", text="Actor Quaternion"
        )

        layout.separator()

        layout.label(text="Custom Properties")

        custom_prop("Game Task")

        custom_prop("Crate Type")

        # Todo: Not 100% sure how to do this one actually, might split up
        custom_prop("Eco Info")

        # layout.label(text="Select an actor to see its properties.", icon="ERROR")

        layout.separator()


classes.append(OBJECT_PT_ActorInfoMenu)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.Scene.actor_properties = bpy.props.PointerProperty(type=ActorProperties)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.actor_properties


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
