# TODO: docstring


##############################################################################
# Imports           Order: 3rd Party Imports, Python Built-ins, Custom Modules
##############################################################################


import bpy
import socket
import threading
import struct
import time


from . import io


##############################################################################
# Constants
##############################################################################

# Bone default constants
SIZE = 1.0
ROTATION = (0, 0, 0)
POSITION = (0, 0, 0)
LENGTH = 1.0

LTT_MSG_POKE = 1
LTT_MSG_INSPECT = 5
LTT_MSG_PRINT = 6
LTT_MSG_PRINT_SYMBOLS = 7
LTT_MSG_RESET = 8
LTT_MSG_CODE = 9
LTT_MSG_SHUTDOWN = 10

##############################################################################
# Properties and Classes
##############################################################################


classes = []  # Initialize the class array to be registered


class REPLButton(bpy.types.Operator):
# Change to PEPL Port to reflect PEPL <-> REPL connection in either GOALC or GK
    """ Tip: Use this to turn any UI into an easy GK or GOALC contact point.
        Like: Sending the expression (:status) to the OpenGOAL REPL, if one is open. """

    # Be careful, operator docstrings are exposed to the user
    # TODO move to contributer docs^

    bl_idname = "wm.repl"  # Unique operator reference name
    bl_label = "Send"  # String for the UI
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator

    clientSocket = None
    packet_stack = []

    gk_port = 8112
    gk2_port = 8113
    gk3_port = 8114
    gkx_port = 8120 # fingers crossed
    goalc_port = 8181

    _timer = None
    refresh = 1/60

    #def __init__(cls):

    def modal(cls, context, event):
        if event.type == 'TIMER':
            #loop functions
            cls.clear_stack()
        return {'PASS_THROUGH'}

    @classmethod
    def create_socket(cls):

        # Create a TCP socket
        cls.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # def enter_disconnected_PEPL(cls, context):
        # A loop which polls once a second for a GOALC or GK on the selected ports
        # It then validates its identity before it connects to it if one is found.
        
    # def validate_port()

    @classmethod
    def bind_port(cls, port):

        # Socket is not created, so create
        if cls.clientSocket is None:
            cls.create_socket()
            io.debug("Opening socket")

            try:
                cls.clientSocket.connect(("127.0.0.1", port))
                io.debug(f"Socket bound to [{port}]")

                # OpenGOAL auto-sends a ping message
                # Capture it and print it
                data = cls.clientSocket.recv(300)
                io.verbose(data.decode())

                # Start stack loop

            # You'll get this error if there's no REPL or GK running.
            except ConnectionRefusedError:
                
                # Reassure the populace
                print(f"No connection could be made, nothing to connect to.")
                
                # Close
                cls.close_socket()

        # Socket is already connected, so no need to connect
        io.verbose("Using open socket")
        return

    @classmethod
    def clear_stack(cls):
        """Executes send-eval-return pattern on the packet stack"""

        # Make loop less opaque
        #io.verbose("No packets")

        # Check if there are any packets in the stack
        if len(cls.packet_stack) > 0:

            io.verbose(f"Stack size: {len(cls.packet_stack)}")
            start_time = time.time()

            # Prepare pointers for after evaluation
            pointers = []

            # Prepare packets to be sent
            packets = []

            # Add them to parallel arrays to keep them aligned
            for signed_packet in cls.packet_stack:
                packets.append(signed_packet['packet'])
                pointers.append(signed_packet['pointer'])

            # Send the command packets all at once
            cls.clientSocket.sendall(b"".join(packets))

            # Clear the packet stack
            cls.packet_stack = []

            # Receive and redirect the responses to associated pointers
            for pointer in pointers:

                # Interpret the response
                response = cls.clientSocket.recv(1024).decode().strip()

                # TODO Redirect the response to the associated pointer that requested it
                print(f"{pointer}: {response}")

            process_time = time.time() - start_time
            io.verbose(f"Stack time: {process_time}")

    @classmethod
    def goalc_packet(cls, expression:str, msg_kind:int):
        """Return packet to be sent to OpenGOAL REPL"""
        
        # Pack up a header
        header = struct.pack('<II', len(expression), msg_kind)

        # Return the packet
        # TODO return packet class instance instead
        return header + expression.encode()

    @classmethod
    def gk_packet(cls, expression:str, ltt_msg_kind:int):
        """Return packet to be sent to OpenGOAL Game instance"""
        
        # Pack header
        header = struct.pack('<IIHBBBHIQ', 
                    len(expression) + 32, # Full struct length              u32=I
                    0xe048,         # 0xe048="D" DECI2 protocol             u16=H
                    0x45,           # 0x45="H" Host source                  u8=B
                    0x05,           # 0x05="E" Emotion Engine destination   u8=B
                    0,              # rsvd, unused?                         u32=I
                    ltt_msg_kind,   # (ListenerToTargetMsgKind)             u8=B
                    0,              # 0 u6, unused?                         u16=H
                    len(expression),# expression size                       u32=I
                    0)              # 0 msg_id, tracks consecutive msgs     u64=Q

        # Return the packet
        # TODO return packet class instance instead
        return header + expression.encode()

    @classmethod
    def send_goalc_packet(cls, expression:str, msg_kind:int):
        """Send a message directly to the REPL"""
        # TODO add packet to stack, send async from there, not here.

        # Connect if needed
        cls.bind_port(cls.goalc_port)

        # Pack up a message
        packet = cls.goalc_packet(expression, msg_kind)

        # Add return address
        signed_packet={'packet': packet, 'pointer': 'pointer1'}

        # Push it to the stack
        cls.packet_stack.append(signed_packet)

        # Send
        #cls.clientSocket.sendall(packet)
        #cls.clear_stack()

        # Pull response data from the socket
        #data = cls.clientSocket.recv(300) # Be more accurate with size?

        # Success
        return True

    @classmethod
    def send_gk_packet(cls, expression:str, ltt_msg_kind:int):
        """Send a message directly to the game instance"""
        # TODO add packet to stack, send async from there, not here.

        # Connect if needed
        cls.bind_port(cls.gk_port)

        # Pack up a message
        packet = cls.gk_packet(expression, ltt_msg_kind)

        # Add return address
        signed_packet={'packet': packet, 'pointer': 'pointer1'}

        # Push it to the stack
        cls.packet_stack.append(signed_packet)
        
        # Success
        return True

    @classmethod
    def send_ping(cls, expression):
        """Send a ping, return connection message"""
        return cls.send_goalc_packet(expression, 0)

    @classmethod
    def send_eval(cls, expression):
        """Send GOAL to be evaluated, return the value in a string"""
        #return cls.send_gk_packet(expression, 9)
        return cls.send_goalc_packet(expression, 10)

    @classmethod
    def send_exit(cls, run_before_exit):
        """Let the REPL know you're disconnecting, return whether successful"""
        return cls.send_goalc_packet(run_before_exit, 20)

    @classmethod
    def close_socket(cls):
        if cls.clientSocket is not None:
            cls.clientSocket.close()
            cls.clientSocket = None
            io.debug("Socket closed")
        
    def execute(cls, context):  # execute() is called when running the operator

        # Grab the repl textbox's contents
        repl_expr = context.scene.level_properties.repl_expr

        # Send the expression
        #response = cls.send_eval(repl_expr)

        # Send a stack of n expressions
        n=1
        for i in range(n):
            response = cls.send_eval(repl_expr)
        
        # Do something with the response
        # TODO - use as confirmation that message arrived
        io.verbose(f"Send success: {response}")

        # Reload an associated file, test
        # ml("goal_src/jak1/engine/target/target-util.gc")

        # Close
        #cls.close_socket()

        cls._timer = context.window_manager.event_timer_add(1/60, window=context.window)
        context.window_manager.modal_handler_add(cls)
        return {'RUNNING_MODAL'}

    def cancel(cls, context):
        context.window_manager.event_timer_remove(cls._timer)
        return {'CANCELLED'}


classes.append(REPLButton)  # Add the class to the array


class Packet:
# Packet designed to emulate DECI2 communication for direct Blender to GK inspect requests
# Test before using


    def __init__(self, len_val, rsvd_val, protocol_val, source_val, destination_val,
                 kind_val, unused_val, message_size_val, message_id_val, address_val):
        self.len = len_val              # u32
        self.rsvd = rsvd_val            # u32
        self.protocol = protocol_val    # u16
        self.source = source_val        # u8
        self.destination = destination_val  # u8
        self.kind = kind_val            # u16
        self.unused = unused_val        # u16
        self.message_size = message_size_val  # u32
        self.message_id = message_id_val  # u64
        self.address = address_val      # int

    def compile(self):
        # Pack the attributes into a binary string
        binary_string = struct.pack("<IIBBHBBHIIQI",
                                    self.len, self.rsvd, self.protocol,
                                    self.source, self.destination, self.kind,
                                    self.unused, self.message_size,
                                    self.message_id, self.address, 0x00)
        return binary_string


class OM_Camera:
    def __init__(self):
        self.camera_object = None

    def create_camera(self, camera_name):
        # Create a new camera object
        bpy.ops.object.camera_add()
        camera = bpy.context.object
        camera.name = camera_name
        self.camera_object = camera

    def pan_camera(self, x, y):
        # Pan the camera by adjusting its location
        if self.camera_object is not None:
            self.camera_object.location.x += x
            self.camera_object.location.y += y

    def follow_path(self, path_object):
        # Make the camera object follow a specific path
        if self.camera_object is not None:
            constraint = self.camera_object.constraints.new('FOLLOW_PATH')
            constraint.target = path_object
            constraint.use_curve_follow = True
            constraint.use_fixed_location = False

    def create_particle_emitter(self, emitter_name):
        """ Tip: Use this is create particles relative to the camera's position.
            Like: If you need a yellow eco blast tracking shot. """

        # Create a particle emitter object
        bpy.ops.object.empty_add(type='ARROWS', radius=1.0)
        emitter = bpy.context.object
        emitter.name = emitter_name

    def set_particle_emitter_settings(self, emitter_name, settings):
        # Set particle emitter settings
        emitter = bpy.data.objects.get(emitter_name)
        if emitter is not None:
            for key, value in settings.items():
                setattr(emitter.particle_systems[0].settings, key, value)


class OM_Bone:
    def __init__(self, bone_name, parent_bone_name=None):
        self.bone_name = bone_name
        self.parent_bone_name = parent_bone_name

        # Create the bone object
        bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
        self.armature_obj = bpy.context.object
        self.armature_obj.name = "Armature"
        bpy.ops.object.mode_set(mode='EDIT')

        # Create the bone
        bpy.ops.armature.bone_primitive_add()
        self.bone = bpy.context.active_bone
        self.bone.name = self.bone_name
        self.bone.use_inherit_rotation = False

        # Set parent bone if specified
        if self.parent_bone_name:
            parent_bone = self.armature_obj.data.edit_bones.get(self.parent_bone_name)
            if parent_bone:
                self.bone.parent = parent_bone

        # Exit edit mode
        bpy.ops.object.mode_set(mode='OBJECT')

    def set_size(self, length):
        self.bone.length = length

    def set_rotation(self, rotation=None):
        if rotation is None:
            rotation = ROTATION
            self.bone.rotation_euler = rotation

    def set_position(self, position):
        self.bone.head = position
        self.bone.tail = position

    def set_bone_layer(self, layer_index, enabled):
        self.bone.layers[layer_index] = enabled

    def link_to_object(self, object_name):
        obj = bpy.data.objects.get(object_name)
        if obj:
            obj.parent = self.armature_obj
            obj.parent_type = 'BONE'
            obj.parent_bone = self.bone_name


##############################################################################
# Functions
##############################################################################


def repl(expression: str):
    """ Tip: Use this to rapidly change an OpenGOAL setting mid-playtest.
        Make Jak's shirt red, etc. """

    # Send an expression to the OpenGOAL REPL, if one is open

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    clientSocket.connect(("127.0.0.1", 8112))
    print(clientSocket)
    data = clientSocket.recv(10)
    print(data.decode())

    header = struct.pack('<II', len(expression), 10)

    clientSocket.sendall(header + expression.encode())


def ml(file_to_reload: str):
    """ Tip: Use this to rapidly reload an OpenGOAL file mid-playtest.
    Like: After editing some GOAL code to the double the number of Jaks so my mom can show you
    how to actually beat the boss over Wifi. """

    repl(f"(ml \"{file_to_reload}\")")


def mi():

    """ Tip: Use this to grab a bone out of the code and link it to an OM one. 
    Like: Attaching Jak's fingers to an animation rig and jumping into a motion tracking rig,
    easily built by buying a Kinect 2, not a Kinect 1, get the bigger one. Do your research. """
    
    # "Make Iso Group"
    repl("(mi)")


def create_and_link_bone():

    """ Tip: Use this to grab a bone out of the code and link it to an OM one. 
    Like: Attaching Jak's fingers to an animation rig and jumping into a motion tracking rig,
    easily achieved by buying a Kinect 2, not a Kinect 1, get the bigger one. """

    # Create a bpy bone object with name "Bone1" and no parent bone
    bone1 = BpyBone("Bone1")

    # Set the size, rotation, and position of the bone
    bone1.set_size(1.0)
    bone1.set_rotation((0, 0, 0))
    bone1.set_position((0, 0, 0))

    # Set the bone layer (layer_index) to be enabled (True)
    bone1.set_bone_layer(0, True)

    # Link an object named "Cube" to the bone
    bone1.link_to_object("Cube")


def create_obj_and_link_bone(self, object_name, bone_name):
    """ Tip: Use this to attach an in-game camera to a Blender camera and track its movement during a cutscene. """

    # Create a new object
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.object
    obj.name = object_name

    # Link it to a specific bone
    armature_obj = bpy.data.objects.get("Armature")
    if armature_obj:
        bpy.context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='POSE')
        bone = armature_obj.pose.bones.get(bone_name)
        if bone:
            bpy.ops.object.mode_set(mode='OBJECT')
            obj

def create_cam_and_link_bone(self, camera_name, bone_name):
    """ Tip: Use this to attach an in-game camera to a Blender camera and attach it to a bone on a camera rig
        and then simulate a dollycam or something. """

    # Create a new camera object
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = camera_name
    self.camera_object = camera

    # Link the camera object to the specified bone
    bone = bpy.context.active_object.pose.bones.get(bone_name)
    if bone:
        bone.custom_shape = camera

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
