##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class ActorType:
    """An OpenGoal actor type"""

    def __init__(cls, label, reference, category):
        cls.label = label  # The name the Blender UI will use for the actor
        cls.reference = reference  # The name OpenGoal uses for the actor
        cls.category = category  # The category


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

    instantiate_actor_types()


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
