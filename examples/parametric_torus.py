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

def addTrackToConstraint(obj, name, target):
	print('addTrackToConstraint called')
	cns = obj.constraints.new('TRACK_TO')
	cns.name = name
	cns.target = target
	cns.track_axis = 'TRACK_NEGATIVE_Z'
	cns.up_axis = 'UP_Y'
	cns.owner_space = 'LOCAL'
	cns.target_space = 'LOCAL'
	return

def createTarget(origin=(0,0,0)):
	bpy.ops.object.add(type='EMPTY', location=origin) # Create target empty
	target = bpy.context.object
	target.name = 'Target'
	return target
	
def createCamera(origin, target):
	print('createCamera called')
	# Create object and camera
	bpy.ops.object.add(type='CAMERA', location=origin)
	obj = bpy.context.object
	obj.name = 'CameraObj'
	cam = obj.data
	cam.name = 'Camera'
	addTrackToConstraint(obj, 'TrackConstraint', target)
	
	# Make this the current camera
	bpy.context.scene.camera = obj
	return obj
	
def createTorus(r0, r1, n=10, m=10, name='Torus', origin=(0,0,0)):
	verts = list()
	faces = list()
	
	# Create uniform n by m grid
	for col in range(m):
		for row in range(n):
			u = row/n 
			v = col/m
			
			# Create surface
			point = ((r0 + r1*cos(tau*v))*cos(tau*u), \
					 (r0 + r1*cos(tau*v))*sin(tau*u), \
					  r1*sin(tau*v))
			verts.append(point)
			
			# Connect first and last vertices on the u and v axis
			rowNext = (row + 1) % n
			colNext = (col + 1) % m
			# Indices for each qued
			faces.append(((col*n) + rowNext, (colNext*n) + rowNext, (colNext*n) + row, (col*n) + row))
			
	print('verts : ' + str(len(verts)))
	print('faces : ' + str(len(faces)))
	
	# Create mesh and object
	mesh = bpy.data.meshes.new(name+'Mesh')
	obj  = bpy.data.objects.new(name, mesh)
	obj.location = origin
	# Link object to scene
	bpy.context.scene.objects.link(obj)
	# Create mesh from given verts and faces
	mesh.from_pydata(verts, [], faces)
	#Update mesh with new data
	mesh.update(calc_edges=True)
	return obj

def setSmooth(obj, smooth=True, level=3):
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
		
def rainbowLights(r=5, n=100, freq=2, energy=0.1):
	for i in range(n):
		t = float(i)/float(n)
		pos = (r*sin(tau*t), r*cos(tau*t), r*sin(freq*tau*t))
		
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
target = createTarget()
camera = createCamera((-10, -10, 10), target)

# Set cursor to (0,0,0)
bpy.context.scene.cursor_location = (0,0,0)

# Create lamps
rainbowLights(10, 300, 3)

# Create object and its material
torus = createTorus(4, 2, 20, 20)
setSmooth(torus)

# Specify folder to save rendering
render_folder = os.path.join(cwd, 'rendering')
if(not os.path.exists(render_folder)):
	os.mkdir(render_folder)

# Render image
rnd = bpy.data.scenes['Scene'].render
rnd.resolution_x = 500
rnd.resolution_y = 500
rnd.resolution_percentage = 100
rnd.filepath = os.path.join(render_folder, 'parametric_torus.png')
bpy.ops.render.render(write_still=True)