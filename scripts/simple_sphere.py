import bpy
import colorsys
from math import sin, cos, pi
from mathutils import Euler
TAU = 2*pi


def rainbow_lights(r=5, n=100, freq=2, energy=100):
    for i in range(n):
        t = float(i)/float(n)
        pos = (r*sin(TAU*t), r*cos(TAU*t), r*sin(freq*TAU*t))

        # Create lamp
        bpy.ops.object.add(type='LIGHT', location=pos)
        obj = bpy.context.object
        obj.data.type = 'POINT'

        # Apply gamma correction for Blender
        color = tuple(pow(c, 2.2) for c in colorsys.hsv_to_rgb(t, 0.6, 1))

        # Set HSV color and lamp energy
        obj.data.color = color
        obj.data.energy = energy


if __name__ == '__main__':
    # Remove all elements
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Set cursor to (0, 0, 0)
    bpy.context.scene.cursor.location = (0, 0, 0)

    # Create camera
    bpy.ops.object.add(type='CAMERA', location=(0, -3.0, 0))
    camera = bpy.context.object
    camera.data.lens = 35
    camera.rotation_euler = Euler((pi/2, 0, 0), 'XYZ')
    
    # Make this the current camera
    bpy.context.scene.camera = camera

    # Create lamps
    rainbow_lights(5, 100, 2, energy=100)

    # Create object
    bpy.ops.mesh.primitive_ico_sphere_add(
        location=(0,0,0),
        subdivisions=3,
        radius=1)
    obj = bpy.context.object
    
    # Add subsurf modifier
    modifier = obj.modifiers.new('Subsurf', 'SUBSURF')
    modifier.levels = 2
    modifier.render_levels = 2
    
    # Smooth surface
    for p in obj.data.polygons:
        p.use_smooth = True

    # Add Glossy BSDF material
    mat = bpy.data.materials.new('Material')
    mat.use_nodes = True
    node = mat.node_tree.nodes[0]
    node.inputs[0].default_value = (0.8, 0.8, 0.8, 1)  # Base color
    node.inputs[4].default_value = 0.5  # Metalic
    node.inputs[7].default_value = 0.5  # Roughness
    obj.data.materials.append(mat)

    # Render image
    scene = bpy.context.scene
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.engine = 'CYCLES'
    #scene.render.engine = 'BLENDER_EEVEE'
    scene.render.filepath = 'rendering/simple_sphere.png'
    bpy.ops.render.render(write_still=True)
