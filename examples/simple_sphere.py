import bpy
import os
import sys
from math import pi
from mathutils import Euler
tau = 2*pi



def getScriptFolder():
	# Check if script is opened in Blender program
	if(bpy.context.space_data == None):
		folder = os.path.dirname(os.path.abspath(__file__))
	else:
		folder = os.path.dirname(bpy.context.space_data.text.filepath)
	return folder

def createSphere(origin=(0,0,0)):
	# Create icosphere
	bpy.ops.mesh.primitive_ico_sphere_add(location=origin)
	obj = bpy.context.object
	return obj
	
	
	
# Get folder of script and add current working directory to path
cwd = getScriptFolder()
sys.path.append(cwd)
import utils
	
# Remove all elements
utils.removeAll()

# Create camera
bpy.ops.object.add(type='CAMERA', location=(0,-3.5,0))
cam = bpy.context.object
cam.rotation_euler = Euler((pi/2,0,0), 'XYZ')
# Make this the current camera
bpy.context.scene.camera = cam

# Create lamps
utils.rainbowLights()

# Create object and its material
sphere = createSphere()
utils.setSmooth(sphere, 3)

# Specify folder to save rendering
render_folder = os.path.join(cwd, 'rendering')
if(not os.path.exists(render_folder)):
	os.mkdir(render_folder)

# Render image
rnd = bpy.data.scenes['Scene'].render
rnd.resolution_x = 500
rnd.resolution_y = 500
rnd.resolution_percentage = 100
rnd.filepath = os.path.join(render_folder, 'simple_sphere.png')
bpy.ops.render.render(write_still=True)
