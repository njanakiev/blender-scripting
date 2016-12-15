import bpy
from math import sin, cos, pi
tau = 2*pi
import colorsys


def addTrackToConstraint(obj, name, target):
	cns = obj.constraints.new('TRACK_TO')
	cns.name = name
	cns.target = target
	cns.track_axis = 'TRACK_NEGATIVE_Z'
	cns.up_axis = 'UP_Y'
	cns.owner_space = 'LOCAL'
	cns.target_space = 'LOCAL'

def createTarget(origin=(0,0,0)):
	bpy.ops.object.add(type='EMPTY', location=origin) # Create target empty
	target = bpy.context.object
	target.name = 'Target'
	return target
		
def createCamera(origin, target=None, lens=35, clip_start=0.1, clip_end=200, type='PERSP', ortho_scale=6):
	# Create object and camera
	camera = bpy.data.cameras.new("Camera")
	camera.lens = lens
	camera.clip_start = clip_start
	camera.clip_end = clip_end
	camera.type = type # 'PERSP', 'ORTHO', 'PANO'
	if(type == 'ORTHO'):
		camera.ortho_scale = ortho_scale
	
	# Link object to scene
	obj = bpy.data.objects.new("CameraObj", camera)
	obj.location = origin
	bpy.context.scene.objects.link(obj)
	bpy.context.scene.camera = obj # Make this the current camera
	
	if(target): addTrackToConstraint(obj, 'TrackConstraint', target)
	return obj

def createLamp(origin, target=None, type='POINT', energy=1, color=(1,1,1)):
	# Lamp types: 'POINT', 'SUN', 'SPOT', 'HEMI', 'AREA'
	bpy.ops.object.add(type='LAMP', location=origin)
	obj = bpy.context.object
	obj.data.type = type
	obj.data.energy = energy
	obj.data.color = color
	
	if(target): addTrackToConstraint(obj, 'TrackConstraint', target)
	return obj
	
def setAmbientOcclusion(ambient_occulusion=True, samples=5, blend_type = 'ADD'):
	# blend_type options: 'ADD', 'MULTIPLY'
	bpy.context.scene.world.light_settings.use_ambient_occlusion = ambient_occulusion
	bpy.context.scene.world.light_settings.ao_blend_type = blend_type
	bpy.context.scene.world.light_settings.samples = samples	

def setSmooth(obj, level=None, smooth=True):
	if(level):
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
		
		# Apply gamma correction for Blender
		color = tuple(pow(float(c) for c in colorsys.hsv_to_rgb(t, 0.6, 1)))
		
		# Set HSV color and lamp energy
		obj.data.color = color
		obj.data.energy = energy

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

def simpleMaterial(diffuse_color):
	mat = bpy.data.materials.new('Material')
	
	# Diffuse
	mat.diffuse_shader = 'LAMBERT'
	mat.diffuse_intensity = 0.9
	mat.diffuse_color = diffuse_color
	
	# Specular
	mat.specular_intensity = 0
	
	return mat
		
def colorRGB_256(color):
	return tuple(pow(float(c)/255.0, 2.2) for c in color)
