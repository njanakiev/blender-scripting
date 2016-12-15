import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix
from math import sqrt
import itertools

# Check if script is opened in Blender program
import os, sys
if(bpy.context.space_data == None):
	cwd = os.path.dirname(os.path.abspath(__file__))
else: 
	cwd = os.path.dirname(bpy.context.space_data.text.filepath)	
# Get folder of script and add current working directory to path
sys.path.append(cwd)
import utils


def tetrahedronPoints(r=1, origin=(0, 0, 0), matrix=Matrix.Identity(3)):
	origin = Vector(origin)
	
	# http://mathworld.wolfram.com/RegularTetrahedron.html
	a = 4*r/sqrt(6)
	h = a*sqrt(6)/3
	points = [( sqrt(3)*a/3,  0, -r/3), \
			  (-sqrt(3)*a/6, -0.5*a, -r/3), \
			  (-sqrt(3)*a/6,  0.5*a, -r/3), \
			  (0, 0, sqrt(6)*a/3 - r/3)]
	
	points = [matrix*Vector(p) + origin for p in points]
	return points
	

def recursiveTetrahedron(bm, points, level=0):
	subTetras = []
	for i in range(len(points)):
		p0 = points[i]
		pK = points[:i] + points[i + 1:]
		subTetras.append([p0] + [(p0 + p)/2 for p in pK])
	
	if 0 < level:
		for subTetra in subTetras:
			recursiveTetrahedron(bm, subTetra, level-1)
	else:
		for subTetra in subTetras:
			verts = [bm.verts.new(p) for p in subTetra]
			faces = [bm.faces.new(face) for face in itertools.combinations(verts, 3)]
			bmesh.ops.recalc_face_normals(bm, faces=faces)
			

# Remove all elements
utils.removeAll()

		
# Creata fractal tetrahedron
bm = bmesh.new()
tetrahedronBasePoints = tetrahedronPoints(5)
recursiveTetrahedron(bm, tetrahedronBasePoints, level=4)
			
# Create obj and mesh from bmesh object
me = bpy.data.meshes.new("TetrahedronMesh")
bm.to_mesh(me)
bm.free()
obj = bpy.data.objects.new("Tetrahedron", me)
bpy.context.scene.objects.link(obj)
bpy.context.scene.update()

	
# Create camera and lamp
target = utils.createTarget((0, 0, 1))
utils.createCamera((-8, 10, 5), target, type='ORTHO', ortho_scale=10)
utils.createLamp((10, -10, 10), target, 'SUN')

# Enable ambient occlusion
utils.setAmbientOcclusion(samples=10)

# Specify folder to save rendering
render_folder = os.path.join(cwd, 'rendering')
if(not os.path.exists(render_folder)):
	os.mkdir(render_folder)

	
# Select colors
palette = [(181,221,201), (218,122,61)]
palette = [utils.colorRGB_256(color) for color in palette]  # Adjust color to Blender

# Set background color of scene
bpy.context.scene.world.horizon_color = palette[0]

# Set material for object
mat = utils.simpleMaterial(palette[1])
obj.data.materials.append(mat)


# Render image
rnd = bpy.data.scenes['Scene'].render
rnd.resolution_x = 500
rnd.resolution_y = 500
rnd.resolution_percentage = 100
rnd.filepath = os.path.join(render_folder, 'fractal_tetrahedron.png')
bpy.ops.render.render(write_still=True)
