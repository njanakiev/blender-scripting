import bpy
import random
from mathutils import Vector
import utils


def createMetaball(origin=(0, 0, 0), n=30, r0=4, r1=2.5):
    metaball = bpy.data.metaballs.new('MetaBall')
    obj = bpy.data.objects.new('MetaBallObject', metaball)
    bpy.context.collection.objects.link(obj)

    metaball.resolution = 0.2
    metaball.render_resolution = 0.05

    for i in range(n):
        location = Vector(origin) + Vector(random.uniform(-r0, r0) for i in range(3))

        element = metaball.elements.new()
        element.co = location
        element.radius = r1

    return obj


if __name__ == '__main__':
    # Remove all elements
    utils.remove_all()

    # Create camera
    target = utils.create_target()
    camera = utils.create_camera((-10, -10, 10), target)

    # Create lights
    utils.rainbowLights(10, 100, 3, energy=100)

    # Create metaball
    obj = createMetaball()
    
    # Create material
    mat = utils.create_material(metalic=0.5)
    obj.data.materials.append(mat)

    # Render scene
    utils.render('rendering', 'metaballs', 512, 512)
