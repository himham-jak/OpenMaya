##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy


##############################################################################
# Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class ActorProperties(bpy.types.PropertyGroup):

    actor_name: bpy.props.StringProperty(
        name="Actor Name",
        description="The name of your object (actor).\nOnly lowercase letters and dashes are allowed.\nDefault: my-level",
        default="my-actor",
        maxlen=1024,
    )

    actor_type: bpy.props.EnumProperty(
        name="Actor Type",
        description="Apply Data to attribute.",
        items=[
            ("collectable", "", ""),
            ("eco-collectable", "", ""),
            ("eco", "", ""),
            ("eco-yellow", "Yellow Eco", ""),
            ("eco-red", "Red Eco", ""),
            ("eco-blue", "Blue Eco", ""),
            ("health", "Green Eco", ""),
            ("eco-pill", "Green Eco Pill", ""),
            ("money", "Precursor Orb", ""),
            ("fuel-cell", "Power Cell", ""),
            ("buzzer", "Scout Fly", ""),
            ("ecovalve", "Eco Valve", ""),
            ("vent", "", ""),
            ("ventyellow", "Yellow Eco Vent", ""),
            ("ventred", "Red Eco Vent", ""),
            ("ventblue", "Blue Eco Vent", ""),
            ("ecovent", "Eco Vent", ""),
            ("vent-wait-for-touch", "", ""),
            ("vent-pickup", "", ""),
            ("vent-standard-event-handler", "", ""),
            ("vent-blocked", "", ""),
            ("ecovalve-init-by-other", "", ""),
            ("*ecovalve-sg*", "", ""),
            ("ecovalve-idle", "", ""),
            ("*eco-pill-count*", "", ""),
            ("birth-pickup-at-point", "", ""),
            ("*buzzer-sg*", "", ""),
            ("fuel-cell-pick-anim", "", ""),
            ("fuel-cell-clone-anim", "", ""),
            ("*fuel-cell-tune-pos*", "", ""),
            ("*fuel-cell-sg*", "", ""),
            ("othercam-init-by-other", "", ""),
            ("fuel-cell-animate", "", ""),
            ("*money-sg*", "", ""),
            ("add-blue-motion", "", ""),
            ("check-blue-suck", "", ""),
            ("initialize-eco-by-other", "", ""),
            ("add-blue-shake", "", ""),
            ("money-init-by-other", "", ""),
            ("money-init-by-other-no-bob", "", ""),
            ("fuel-cell-init-by-other", "", ""),
            ("fuel-cell-init-as-clone", "", ""),
            ("buzzer-init-by-other", "", ""),
            ("crate-post", "", ""),
            ("*crate-iron-sg*", "", ""),
            ("*crate-steel-sg*", "", ""),
            ("*crate-darkeco-sg*", "", ""),
            ("*crate-barrel-sg*", "", ""),
            ("*crate-bucket-sg*", "", ""),
            ("*crate-wood-sg*", "", ""),
            ("*CRATE-bank*", "", ""),
            ("crate-standard-event-handler", "", ""),
            ("crate-init-by-other", "", ""),
            ("crate-bank", "", ""),
            (
                "crate",
                "",
                "",
            ),  # eco-info [item,quantity] item: 1=yellow 2=red 3=green 4=cell 5=orb 6=blue 7=pill 8=fly 9+=empty, enames=crate/iron,steel,bucket,barrel
            ("barrel", "", ""),
            ("bucket", "", ""),
            ("crate-buzzer", "Scout Fly Box", ""),
            ("pickup-spawner", "", ""),
            ("double-lurker", "Double Lurker", ""),
            ("evilbro", "Gol", ""),
            ("evilsis", "Maya", ""),
            ("explorer", "Explorer", ""),
            ("farmer", "Farmer", ""),
            ("balloon", "Balloon", ""),
            ("spike", "Spike", ""),
            ("crate-darkeco-cluster", "Cluster of Dark Eco Crates", ""),
            ("flutflut", "Flut Flut", ""),
            ("geologist", "Geologist", ""),
            ("hopper", "Hopper", ""),
            ("junglesnake", "Jungle Snake", ""),
            ("kermit", "Kermit", ""),
            ("lurkercrab", "Lurker Crab", ""),
            ("lurkerpuppy", "Lurker Puppy", ""),
            ("lurkerworm", "Lurker Worm", ""),
            ("mother-spider", "Mother Spider", ""),
            ("muse", "Muse", ""),
            ("swamp-rat", "Swamp Rat", ""),
            ("yeti", "Yeti", ""),
            ("yakow", "Yakow", ""),
            ("orbit-plat", "Orbiting Platform", ""),
            ("steam-cap", "Steam Cap Platform", ""),
            ("citb-plat", "Citadel B Platform", ""),
            ("citb-button", "Citadel B Button", ""),
            ("citb-drop-plat", "Citadel B Drop Platform", ""),
            ("wall-plat", "Wall Platform", ""),
            ("wedge-plat", "Wedge Platform", ""),
            ("wedge-plat-outer", "Wedge Platform Outer", ""),
            ("puffer", "Puffer", ""),
            ("babak", "Gorilla", ""),
            ("babak-with-cannon", "Gorilla with Cannon", ""),
            ("seaweed", "Seaweed", ""),
            ("ropebridge", "Rope Bridge", ""),
        ],
    )

    actor_location: bpy.props.FloatVectorProperty(
        name="Actor Location",
        description="The location in 3d space to place your object (actor).\nDefault: -21.6238,20.0496,17.1191",
        default=(-21.6238, 20.0496, 17.1191),
        min=0.0,
        max=25.0,
    )

    actor_rotation: bpy.props.FloatVectorProperty(
        name="Actor Rotation",
        description="The quaternion rotation in 3d space to place your object (actor.\nDefault: 0,0,0,1",
        default=(0.0, 0.0, 0.0),  # Blender doesn't want me to make a 4d vector
        min=0.0,
        max=1.0,
    )


classes.append(ActorProperties)  # Add the class to the array


class OBJECT_PT_ActorInfoMenu(bpy.types.Panel):
    """"""

    bl_idname = "OBJECT_PT_ActorInfoMenu"
    bl_label = "Actor Info"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Level Editor"
    bl_context = "objectmode"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        actor_properties = scene.actor_properties

        layout.prop(context.active_object, "name", text="Actor Name")
        layout.prop(actor_properties, "actor_type")  # dummy
        layout.prop(context.active_object, "type")

        # these properties auto populate
        layout.prop(context.active_object, "location", text="Actor Location")
        layout.prop(
            context.active_object, "rotation_quaternion", text="Actor Rotation"
        )  # this won't display properly unless the object is in quaternion mode, so I force all actors into quat mode when added

        layout.label(text="Select an actor to see its properties.", icon="ERROR")

        layout.separator()


classes.append(OBJECT_PT_ActorInfoMenu)  # Add the class to the array


##############################################################################
# Functions
##############################################################################


##############################################################################
# Registration
##############################################################################


def register():

    for cls in classes:  # Register all the classes
        bpy.utils.register_class(cls)

    bpy.types.Scene.actor_properties = bpy.props.PointerProperty(type=ActorProperties)


def unregister():

    for cls in reversed(classes):  # Unregister all the classes
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.actor_properties


# if __name__ == "__main__":  # For internal Blender script testing
#    register()
