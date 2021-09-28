import bpy
from math import sin, cos, pi
TAU = 2*pi
import utils


# Create a function for the u, v surface parameterization from r0 and r1
def torus_surface(r0, r1):
    def surface(u, v):
        point = ((r0 + r1*cos(TAU*v))*cos(TAU*u), \
                 (r0 + r1*cos(TAU*v))*sin(TAU*u), \
                  r1*sin(TAU*v))
        return point
    return surface


# Create an object from a surface parameterization
def create_surface(surface, n=10, m=10, origin=(0,0,0), name='Surface'):
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
            row_next = (row + 1) % n
            col_next = (col + 1) % m
            # Indices for each qued
            faces.append((
                (col*n) + row_next, 
                (col_next*n) + row_next, 
                (col_next*n) + row, 
                (col*n) + row
            ))

    print('verts : ' + str(len(verts)))
    print('faces : ' + str(len(faces)))

    # Create mesh and object
    mesh = bpy.data.meshes.new(name+'Mesh')
    obj  = bpy.data.objects.new(name, mesh)
    obj.location = origin
    # Link object to scene
    bpy.context.collection.objects.link(obj)
    # Create mesh from given verts and faces
    mesh.from_pydata(verts, [], faces)
    #Update mesh with new data
    mesh.update(calc_edges=True)
    return obj


if __name__ == '__main__':
    # Remove all elements
    utils.remove_all()

    # Create camera
    target = utils.create_target()
    camera = utils.create_camera((-12, -12, 12), target, lens=50)

    # Set cursor to (0, 0, 0)
    bpy.context.scene.cursor.location = (0, 0, 0)

    # Create lamps
    utils.rainbowLights(10, 100, 3, energy=300)

    # Create object
    obj = create_surface(torus_surface(4, 2), 20, 20)

    # Create material
    mat = utils.create_material(metalic=0.5)
    obj.data.materials.append(mat)

    # Smooth surface and add subsurf modifier
    utils.set_smooth(obj, 2)
    
    # Render scene
    utils.render(
        'rendering', 'parametric_torus', 500, 500,
        render_engine='CYCLES')
