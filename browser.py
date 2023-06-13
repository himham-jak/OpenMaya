##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import os


##############################################################################
# Constants
##############################################################################


SCAN_DIR = "D:\\Git\\jak-project"


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class OBJECT_PT_BrowserMenu(bpy.types.Panel):
    """"""

    bl_idname = "OBJECT_PT_BrowserMenu"
    bl_label = "Browser"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OpenMaya"
    bl_context = "mesh_edit"

    def draw(self, context):

        layout = self.layout
        obj = context.object

        draw_props(self, context)

classes.append(OBJECT_PT_BrowserMenu)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


def draw_props(self, context):

    layout = self.layout
    obj = context.object
    
    # Draw an Error
    layout.label(text="Unable to open blah")

    # Clean the paths
    _, clean_root = SCAN_DIR.rsplit("\\", 1)
    clean_ancestor = clean_root.replace("-", "_") # This cleans the var names imperfectly

    # Draw the folder itself being expanded
    ancestor = draw_item(layout, f'{clean_ancestor}/', 'Root', 0.01, 0.95)

    # Walk all files, drawing UI elements in browser
    for root, dirs, files in os.walk(SCAN_DIR):

        # Files directly in the root/ancestor
        for file in files:

            # Skip hidden (.) files
            if file[0] == ".": 
                continue

            # Get parent alone
            _, parent = root.rsplit("\\", 1)

            # Skip files not in root
            if parent != clean_root:
                continue

            name, ext = os.path.splitext(file)

            clean_name = name.replace("-", "_")

            exec(f"{clean_name} = draw_item(ancestor, '{name}', '{ext} file', 0.05, 0.95)")

        for folder in dirs:

            # Skip hidden (.) folders
            if folder[0] == ".": 
                continue

            clean_name = folder.replace("-", "_") # This cleans the var names imperfectly
            exec(f"{clean_name} = draw_folder(ancestor, f'{folder}/')")

        for file in files:

            # Skip hidden (.) files
            if file[0] == ".": 
                continue

            # Get parent alone
            _, parent = root.rsplit("\\", 1)

            # Skip files in root
            if parent == clean_root:
                continue

            clean_parent = parent.replace("-", "_")

            name, ext = os.path.splitext(file)

            clean_name = name.replace("-", "_")

            print(f"{name}{ext} added to {clean_parent}")
            exec(f"{clean_name} = draw_item({clean_parent}, '{name}', '{ext} file', 0.05, 0.95)")


def draw_item(layout, name, goal_type, lmargin, rmargin):

    cols = layout.column()
    vsplit1 = cols.split(factor=rmargin)
    vsplit2 = vsplit1.split(factor=(lmargin/rmargin))

    nullcol = vsplit2.column()

    box = vsplit2.box()
    vsplit3 = box.split(factor=0.75)
    col1 = vsplit3.column()
    col2 = vsplit3.column()

    col1.alignment = 'LEFT'
    col1.label(text=name)
    # Put some standard ops here

    col2.alignment = 'RIGHT'
    col2.label(text=goal_type)

    layout.separator()

    return cols


def draw_folder(layout, name):

    return draw_item(layout, name, "Folder", 0.025, 0.95)


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