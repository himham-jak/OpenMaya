bl_info = {
    "name": "Test Multifile Addon",
    "category": "All",
    "version": (0, 0, 1),
    "blender": (2, 78, 0),
}

module_names = ["addCube", "addCubePanel"]

import sys
import importlib

module_full_names = {}
for current_module_name in module_names:
    if "DEBUG_MODE" in sys.argv:
        module_full_names[current_module_name] = "{}".format(current_module_name)
    else:
        module_full_names[current_module_name] = "{}.{}".format(
            __name__, current_module_name
        )

for current_module_full_name in module_full_names.values():
    if current_module_full_name in sys.modules:
        importlib.reload(sys.modules[current_module_full_name])
    else:
        globals()[current_module_full_name] = importlib.import_module(
            current_module_full_name
        )
        setattr(globals()[current_module_full_name], "module_names", module_full_names)


def register():
    for current_module_name in module_full_names.values():
        if current_module_name in sys.modules:
            if hasattr(sys.modules[current_module_name], "register"):
                sys.modules[current_module_name].register()


def unregister():
    for current_module_name in module_full_names.values():
        if current_module_name in sys.modules:
            if hasattr(sys.modules[current_module_name], "unregister"):
                sys.modules[current_module_name].unregister()


if __name__ == "__main__":
    register()
