##############################################################################
# Imports
##############################################################################


import bpy
from dataclasses import dataclass


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


@dataclass
class ActorType:
    """An OpenGoal actor type"""

    label: str = "default-label"  # The name the Blender UI will use for the actor
    reference: str = "default-ref"  # The name OpenGoal uses for the actor
    category: str = "default-cat"  # The category


# Standard classes don't register


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


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
