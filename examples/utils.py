import bpy
from math import sin, cos, pi
tau = 2*pi
from mathutils import Color, Euler


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

def setSmooth(obj, level=2, smooth=True):
	# Add subsurf modifier
	modifier = obj.modifiers.new('Subsurf', 'SUBSURF')
	modifier.levels = level
	modifier.render_levels = level
	
	# Smooth surface
	mesh = obj.data
	for p in mesh.polygons:
		p.use_smooth = smooth	
	
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

def removeAll(type=None):
	# Possible type: ‘MESH’, ‘CURVE’, ‘SURFACE’, ‘META’, ‘FONT’, ‘ARMATURE’, ‘LATTICE’, ‘EMPTY’, ‘CAMERA’, ‘LAMP’
	
	if(type):
		bpy.ops.object.select_all(action='DESELECT')
		bpy.ops.object.select_by_type(type=type)
		bpy.ops.object.delete()
	else:
		# Remove all elements in scene
		bpy.ops.object.select_by_layer()
		bpy.ops.object.delete(use_global=False)
		
		