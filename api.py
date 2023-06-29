# TODO: docstring


##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import socket
import struct


##############################################################################
# Constants
##############################################################################


##############################################################################
# Properties and Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class REPLButton(bpy.types.Operator):
    """Send an expression to the OpenGOAL REPL, if one is open"""  # Be careful, operator docstrings are exposed to the user

    bl_idname = "wm.repl"  # Unique operator reference name
    bl_label = "Send"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    def execute(cls, context):  # execute() is called when running the operator

        # Grab the repl textbox's contents
        repl_expr = context.scene.level_properties.repl_expr

        # Send the expression
        repl(repl_expr)

        # Reload an associated file, test
        ml("goal_src/jak1/engine/target/target-util.gc")

        return {"FINISHED"}  # Let Blender know the operator finished successfully


classes.append(REPLButton)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


def repl(expression: str):
    #Send an expression to the OpenGOAL REPL, if one is open

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    clientSocket.connect(("127.0.0.1", 8112))
    #print(clientSocket)
    data = clientSocket.recv(0)
    #print(data.decode())

    header = struct.pack('<II', len(expression), 10)

    clientSocket.sendall(header + expression.encode())


def ml(file_to_reload: str):
    repl(f"(ml \"{file_to_reload}\")")


def mi():
    repl("(mi)")

##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
