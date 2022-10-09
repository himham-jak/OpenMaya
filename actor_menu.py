##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


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

        def custom_prop(name, parent=layout):

            if bpy.data.objects[bpy.context.object.data.name].get(name) is not None:
                parent.prop(
                    bpy.data.objects[bpy.context.object.data.name], f'["{name}"]'
                )

        # Only populate the actor info if something is selected and it's an actor
        if context.active_object and ("Actor Type" in context.active_object.keys()):

            layout.prop(context.active_object, "name", text="Actor Name")

            etype = layout.row()
            etype.enabled = False

            custom_prop("Actor Type", etype)

            layout.prop(context.active_object, "location", text="Actor Translation")

            # This won't display properly unless the object is in quaternion mode, so I force all actors into quat mode when added
            layout.prop(
                context.active_object, "rotation_quaternion", text="Actor Quaternion"
            )

            layout.separator()

            layout.label(text="Custom Properties")

            # Show all of the custom properties
            for key, value in context.active_object.items():
                if not key == "Actor Type":
                    custom_prop(key)

        # Display if something other than an actor is selected
        else:
            layout.label(text="Select an actor to see its properties.", icon="ERROR")

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


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.actor_properties


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
