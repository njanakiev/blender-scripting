import bpy
import os
import sys
from math import sin, cos, pi
tau = 2*pi



def getScriptFolder():
	# Check if script is opened in Blender program
	if(bpy.context.space_data == None):
		folder = os.path.dirname(os.path.abspath(__file__))
	else:
		folder = os.path.dirname(bpy.context.space_data.text.filepath)	
	return folder

	
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


	
# Get folder of script and add current working directory to path
cwd = getScriptFolder()
sys.path.append(cwd)
import utils
	
# Remove all elements
utils.removeAll()

# Create camera
target = utils.createTarget()
camera = utils.createCamera((-10, -10, 10), target)

# Set cursor to (0,0,0)
bpy.context.scene.cursor_location = (0,0,0)

# Create lamps
utils.rainbowLights(10, 300, 3)

# Create object
torus = createTorus(4, 2, 20, 20)
utils.setSmooth(torus)

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