import bpy
import bmesh
import numpy as np
import scipy.spatial as spatial
from random import random
from mathutils import Vector, Matrix
import colorsys
import utils


# Convert hsv values to gamma corrected rgb values
# Based on: http://stackoverflow.com/questions/17910543/convert-gamma-rgb-curves-to-rgb-curves-with-no-gamma/
def convert_hsv(hsv):
    return tuple(pow(val, 2.2) for val in colorsys.hsv_to_rgb(*hsv))


def voronoi_landscape(n=1000, w=10, h=5):
    # Create voronoi structure
    points = np.random.normal(size=(n, 2))/4
    vor = spatial.Voronoi(points)
    verts, regions = vor.vertices, vor.regions

    # Filter unused voronoi regions
    regions = [region for region in regions
                if not -1 in region and len(region) > 0]
    regions = [region for region in regions
                if np.all([np.linalg.norm(verts[i]) < 1.2 for i in region])]

    # Create faces from voronoi regions
    bm = bmesh.new()
    vDict, faces = {}, []
    for region in regions:
        for idx in region:
            if not idx in vDict:
                x, y, z = verts[idx, 0]*w, verts[idx, 1]*w, 0
                vert = bm.verts.new((x, y, z))
                vDict[idx] = vert

        face = bm.faces.new(tuple(vDict[i] for i in region))
        faces.append(face)

    bmesh.ops.recalc_face_normals(bm, faces=faces)

    # Extrude faces randomly
    top_faces = []
    for face in faces:
        r = bmesh.ops.extrude_discrete_faces(bm, faces=[face])
        f = r['faces'][0]
        top_faces.append(f)
        bmesh.ops.translate(bm, vec=Vector((0, 0, random()*h)), verts=f.verts)
        center = f.calc_center_bounds()
        bmesh.ops.scale(bm, vec=Vector((0.8, 0.8, 0.8)), verts=f.verts, space=Matrix.Translation(-center))

    # Create list of random colors based on a range for each channel
    #colorRange = [[0.7, 0.9], [0.7, 0.8], [0.8, 0.9]] # Pink
    colorRange = [[0.5, 0.7], [0.7, 0.8], [0.8, 0.9]] # Blue
    #colorRange = [[0.05, 0.15], [0.7, 0.8], [0.8, 0.9]] # Yellow
    nColors = 20
    colors = np.random.random((nColors, 3))
    for i, r in zip(range(nColors), colorRange):
        print(r)
        colors[:, i] = (r[1] - r[0])*colors[:, i] + r[0]

    # Assign material index to each bar
    for face in top_faces:
        idx = np.random.randint(len(colors))
        face.material_index = idx
        for edge in face.edges:
            for f in edge.link_faces:
                f.material_index = idx

    # Create obj and mesh from bmesh object
    me = bpy.data.meshes.new("VornoiMesh")
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new("Voronoi", me)
    bpy.context.scene.objects.link(obj)
    bpy.context.scene.update()

    # Create and assign materials to object
    for color in colors:
        mat = bpy.data.materials.new('Material')
        mat.diffuse_color = convert_hsv(color)
        mat.diffuse_intensity = 0.9
        obj.data.materials.append(mat)


if __name__ == '__main__':
    print(__file__)

    # Remove all elements
    utils.removeAll()

    # Create object
    voronoi_landscape()

    # Create camera and lamp
    target = utils.target((0, 0, 3))
    utils.camera((-8, -12, 11), target, type='ORTHO', ortho_scale=5)
    utils.lamp((10, -10, 10), target=target, type='SUN')

    # Enable ambient occlusion
    utils.setAmbientOcclusion(samples=10)

    # Render scene
    utils.renderToFolder('rendering', 'vornoi_landscape', 500, 500)
