bl_info = {
    "name": "OpenMaya",
    "description": "Level editing tools for the OpenGoal version of the Jak and Daxter series.",
    "author": "himham, tripp",
    "version": (0, 0, 1),
    "blender": (3, 3, 0),
    "location": "View3D > N-Toolbar > Level Info",
    "warning": "Alpha Build",
    "doc_url": "https://github.com/himham-jak/OpenMaya",
    "tracker_url": "https://github.com/himham-jak/OpenMaya/issues",
    "support": "COMMUNITY",
    "category": "Development",
}


modules = ["example_file"]  # <module_name>.py


##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


for module in modules:  # Import all modules listed in the modules array
    try:
        exec(f"from . import {module}")
        print(f"Importing {module}.py")
    except Exception as e:
        print(e)


##############################################################################
# Registration
##############################################################################


def register():

    for module in modules:  # Register all the modules
        try:
            exec(f"{module}.register()")
            print(f"Registering {module}.py")
        except Exception as e:
            print(e)


def unregister():

    for module in modules:  # Unregister all the modules
        try:
            exec(f"{module}.unregister()")
            print(f"Unregistering {module}.py")
        except Exception as e:
            print(e)


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
