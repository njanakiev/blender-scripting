import bpy
import os
from math import sin, cos, pi
from mathutils import Color, Euler
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

def setSmooth(obj, level=2, smooth=True):
	# Add subsurf modifier
	modifier = obj.modifiers.new('Subsurf', 'SUBSURF')
	modifier.levels = level
	modifier.render_levels = level
	
	# Smooth surface
	mesh = obj.data
	for p in mesh.polygons:
		p.use_smooth = smooth	
	
def createMaterial(name):
	mat = bpy.data.materials.new(name)
	
	# Diffuse color component
	mat.diffuse_color = (1.0, 1.0, 1.0)
	mat.diffuse_shader = 'LAMBERT'
	mat.diffuse_intensity = 0.8
	
	# Specular color component
	mat.specular_color = (1.0, 1.0, 1.0)
	mat.specular_shader = 'COOKTORR'
	mat.specular_intensity = 0.8
	mat.specular_hardness = 100
	return mat
    
def rainbowLights(r=5, n=100, energy=0.1, f=2):
	for i in range(n):
		t = float(i)/float(n)
		pos = (r*sin(tau*t), r*cos(tau*t), r*sin(f*tau*t))
		
		# Create lamp
		bpy.ops.object.add(type='LAMP', location=pos)
		obj = bpy.context.object
		obj.data.type = 'POINT'
		
		# Set HSV color and lamp energy
		c = Color()
		c.hsv = (t, 0.6, 1)
		obj.data.color = c
		obj.data.energy = energy

def removeAll(type):
	# Possible type: ‘MESH’, ‘CURVE’, ‘SURFACE’, ‘META’, ‘FONT’, ‘ARMATURE’, ‘LATTICE’, ‘EMPTY’, ‘CAMERA’, ‘LAMP’
	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_by_type(type=type)
	bpy.ops.object.delete()


	
# Get folder of script
cwd = getScriptFolder()
	
# Remove all elements
bpy.ops.object.select_by_layer()
bpy.ops.object.delete(use_global=False)

# Create camera
bpy.ops.object.add(type='CAMERA', location=(0,-3.5,0))
cam = bpy.context.object
cam.rotation_euler = Euler((pi/2,0,0), 'XYZ')
# Make this the current camera
bpy.context.scene.camera = cam

# Set cursor to (0,0,0)
bpy.context.scene.cursor_location = (0,0,0)

# Create lamps
rainbowLights()

# Create object and its material
sphere = createSphere()
setSmooth(sphere, 3)
mat = createMaterial('Mat')
if sphere.data.materials: sphere.data.materials[0] = mat
else: sphere.data.materials.append(mat)

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