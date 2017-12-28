import bpy
import bmesh
import numpy as np
import scipy.spatial as spatial
from mathutils import Vector, Matrix
import utils


def VoronoiSphere(bm, points, r=2, offset=0.02, numMaterials=1):
    # Calculate 3D Voronoi diagram
    vor = spatial.Voronoi(points)

    facesDict = {}
    for (idx_p0, idx_p1), ridge_vertices in zip(vor.ridge_points, vor.ridge_vertices):
        if -1 in ridge_vertices: continue
        if idx_p0 not in facesDict:
            facesDict[idx_p0] = []
        if idx_p1 not in facesDict:
            facesDict[idx_p1] = []

        facesDict[idx_p0].append(ridge_vertices)
        facesDict[idx_p1].append(ridge_vertices)

    for idx_point in facesDict:
        region = facesDict[idx_point]
        center = Vector(vor.points[idx_point])
        if len(region) <= 1: continue

        # Skip all Voronoi regions outside of radius r
        skip = False
        for faces in region:
            for idx in faces:
                p = vor.vertices[idx]
                if np.linalg.norm(p) > r:
                    skip = True
                    break

        if not skip:
            vertsDict = {}
            material_index = np.random.randint(numMaterials)

            for faces in region:
                verts = []
                for idx in faces:
                    p = Vector(vor.vertices[idx])
                    if idx not in vertsDict:
                        v = center - p
                        v.normalize()
                        vert = bm.verts.new(p + offset*v)
                        verts.append(vert)
                        vertsDict[idx] = vert
                    else:
                        verts.append(vertsDict[idx])

                face = bm.faces.new(verts)
                face.material_index = material_index

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)


if __name__ == '__main__':
    print(__file__)

    # Remove all elements
    utils.removeAll()

    # Set ambient occlusion
    utils.setAmbientOcclusion()

    # Create camera and lamp
    utils.simpleScene((0, 0, 0), (6, 0, 0), (-5, 5, 10))

    # Color palette
    # http://www.colourlovers.com/palette/1189317/Rock_Mint_Splash
    palette = [(89, 91, 90), (20, 195, 162), (13, 229, 168),
               (124, 244, 154), (184, 253, 153)]
    palette = [utils.colorRGB_256(color) for color in palette]

    # Set background color of scene
    bpy.context.scene.world.horizon_color = palette[0]

    # Create Voronoi Sphere
    n, r = 2000, 2
    points = (np.random.random((n, 3)) - 0.5)*2*r
    bm = bmesh.new()
    VoronoiSphere(bm, points, r, numMaterials=len(palette)-1)
    obj = utils.bmeshToObject(bm)

    # Apply materials to object
    for color in palette[1:]:
        mat = utils.simpleMaterial(color)
        obj.data.materials.append(mat)

    # Render scene
    utils.renderToFolder('rendering', 'voronoi_sphere', 500, 500)
