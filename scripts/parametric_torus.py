import bpy
from math import sin, cos, pi
TAU = 2*pi
import utils


# Create a function for the u, v surface parameterization from r0 and r1
def torusSurface(r0, r1):
    def surface(u, v):
        point = ((r0 + r1*cos(TAU*v))*cos(TAU*u), \
                 (r0 + r1*cos(TAU*v))*sin(TAU*u), \
                  r1*sin(TAU*v))
        return point
    return surface

# Create an object from a surface parameterization
def createSurface(surface, n=10, m=10, origin=(0,0,0), name='Surface'):
    verts = list()
    faces = list()

    # Create uniform n by m grid
    for col in range(m):
        for row in range(n):
            u = row / n
            v = col / m

            # Surface parameterization
            point = surface(u, v)
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


if __name__ == '__main__':
    # Remove all elements
    utils.removeAll()

    # Create camera
    target = utils.target()
    camera = utils.camera((-10, -10, 10), target)

    # Set cursor to (0, 0, 0)
    bpy.context.scene.cursor_location = (0, 0, 0)

    # Create lamps
    utils.rainbowLights(10, 300, 3)

    # Create object
    torus = createSurface(torusSurface(4, 2), 20, 20)
    utils.setSmooth(torus, 2)

    # Render scene
    utils.renderToFolder('rendering', 'parametric_torus', 500, 500)
