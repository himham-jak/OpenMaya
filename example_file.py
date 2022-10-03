# Imports


import bpy


# Classes


classes = []  # Initialize the class array to be registered


class ObjectMoveX(bpy.types.Operator):
    bl_idname = "object.move_x"  # Unique operator reference name
    bl_label = "Move X by One"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    def execute(self, context):  # execute() is called when running the operator

        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0

        return {"FINISHED"}  # Lets Blender know the operator finished successfully


classes.append(ObjectMoveX)


# Functions


def menu_func(self, context):
    self.layout.operator(ObjectMoveX.bl_idname)


# Registration


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_object.append(
        menu_func
    )  # Adds the new operator to an existing menu


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":
#    register()
