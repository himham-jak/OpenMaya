bl_info = {
    "name": "OpenMaya",
    "blender": (3, 3, 0),
    "category": "Development",
    "version": (0, 0, 1),
}


modules = ["example_file"]


# Imports


for module in modules:
    try:
        exec(f"from . import {module}")
        print(f"Importing {module}.py")
    except Exception as e:
        print(e)


# Registration


def register():

    import importlib

    for module in modules:
        try:
            exec(f"{module}.register()")
            print(f"Registering {module}.py")
        except Exception as e:
            print(e)


def unregister():

    for module in modules:
        try:
            exec(f"{module}.unregister()")
            print(f"Unregistering {module}.py")
        except Exception as e:
            print(e)


# if __name__ == "__main__":
#    register()
