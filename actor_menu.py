##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy

from . import save_actor


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
    bl_category = "OpenMaya"
    bl_context = "objectmode"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        obj = context.active_object

        def custom_prop(name, parent=layout):

            if bpy.data.objects[bpy.context.object.data.name].get(name) is not None:
                parent.prop(
                    bpy.data.objects[bpy.context.object.data.name], f'["{name}"]'
                )

        # Only populate the actor info if something is selected and it's an actor
        if obj.select_get() and ("Actor Type" in context.active_object.keys()):

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
                if key not in [
                    "Actor Type",
                    "Mesh",
                    "Icon",
                    "JSON Category",
                    "JSON Index",
                ]:
                    custom_prop(key)

            # Provide the option to save the actor as a preset
            # layout.operator("wm.save_actor")

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
