import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix
from math import sqrt
import itertools as it
import utils


def tetrahedron_points(r=1, origin=(0, 0, 0)):
    origin = Vector(origin)

    # Formulas from http://mathworld.wolfram.com/RegularTetrahedron.html
    a = 4*r/sqrt(6)
    points = [( sqrt(3)*a/3,  0, -r/3), \
              (-sqrt(3)*a/6, -0.5*a, -r/3), \
              (-sqrt(3)*a/6,  0.5*a, -r/3), \
              (0, 0, sqrt(6)*a/3 - r/3)]

    points = [Vector(p) + origin for p in points]
    return points


def recursive_tetrahedron(bm, points, level=0):
    sub_tetras = []
    for i in range(len(points)):
        p0 = points[i]
        pK = points[:i] + points[i + 1:]
        sub_tetras.append([p0] + [(p0 + p)/2 for p in pK])

    if 0 < level:
        for subTetra in sub_tetras:
            recursive_tetrahedron(bm, subTetra, level-1)
    else:
        for subTetra in sub_tetras:
            verts = [bm.verts.new(p) for p in subTetra]
            faces = [bm.faces.new(face) for face in it.combinations(verts, 3)]
            bmesh.ops.recalc_face_normals(bm, faces=faces)


if __name__ == '__main__':
    # Remove all elements
    utils.remove_all()

    # Creata fractal tetrahedron
    bm = bmesh.new()
    tetrahedron_base_points = tetrahedron_points(5)
    recursive_tetrahedron(bm, tetrahedron_base_points, level=4)

    # Create obj and mesh from bmesh object
    mesh = bpy.data.meshes.new("TetrahedronMesh")
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("Tetrahedron", mesh)
    bpy.context.collection.objects.link(obj)

    # Create camera and lamp
    target = utils.create_target((0, 0, 1))
    utils.create_camera((-8, 10, 5), target, type='ORTHO', ortho_scale=10)
    utils.create_light((10, -10, 10), target=target, type='SUN', energy=100)

    # Select colors
    palette = [(181, 221, 201, 255), (218, 122, 61, 255)]
    palette = [utils.colorRGB_256(color) for color in palette]  # Adjust color to Blender

    # Set background color of scene
    bpy.context.scene.world.node_tree.nodes["Background"] \
        .inputs[0].default_value = palette[0]

    # Set material for object
    mat = utils.create_material(palette[1])
    obj.data.materials.append(mat)

    # Render scene
    utils.render(
        'rendering', 'tetrahedron_fractal', 500, 500, 
        render_engine='CYCLES')
