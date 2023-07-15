# TODO: docstring


##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy


##############################################################################
# Constants
##############################################################################


##############################################################################
# Properties and Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class TOPBAR_MT_custom_menu(bpy.types.Menu):
    """ Tip: Use this to add a header dropdown menu to the topbar of Blender.
        Like: Adding Preferences to the topbar because Edit > Preferences is so annoying. """
    
    bl_label = "Custom Menu"
    bl_idname = "view3D.custom_menu"

    #Methods
    # Add to File menu top left
	#bpy.types.TOPBAR_MT_editor_menus.append(draw_item)

	# Add to Tabs and top right
	#bpy.types.TOPBAR_HT_upper_bar.append(draw_item)

	# Add to ObjectMode Header
	#bpy.types.VIEW3D_MT_object.append(draw_item)

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.primitive_cube_add")

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_custom_menu")

bpy.utils.register_class(TOPBAR_MT_custom_menu)


class TOPBAR_MT_custom_sub_menu(bpy.types.Menu):
    """ Tip: Use this to populate a ropbar dropdown menu at the top of Blender.
        Like: Adding File > Import > VAGWAD. """
        
    bl_label = "Sub Menu"
    bl_idname = "view3D.custom_sub_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.primitive_cube_add")

bpy.utils.register_class(TOPBAR_MT_custom_sub_menu)


class OM_Header(bpy.types.Header):
    """ Tip: Use this to create a new category of editor panels.
    	Like: If you registered OpenMaya as a new category in layout.template_header()
    	which is the Editor Type dropdown. """


    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        layout = self.layout

        # Add your custom panel to the header
        layout.menu("TOPBAR_MT_custom_menu", text="Custom Panel", icon='PLUGIN')

#TODO fix
bpy.utils.register_class(OM_Header)


##############################################################################
# Functions
##############################################################################


def draw_item(self, context):
    layout = self.layout
    layout.menu(TOPBAR_MT_custom_menu.bl_idname)


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
