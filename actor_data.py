##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class ActorType():
    """An OpenGoal actor type"""

    __init__(cls, label, reference, category):
        label = cls.label  # The name the Blender UI will use for the actor
        reference = cls.reference  # The name OpenGoal uses for the actor
        category = cls.category  # The category


classes.append(ActorType)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


def instantiate_actor_types():

    actors = []  # Initialize the actor array to be instantiated

    actor = ActorType("Precursor Orb","money","Collectible")
    actors.append(actor)


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    instantiate_actor_types()
    print(f"Test: {actors[0].label}")


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
