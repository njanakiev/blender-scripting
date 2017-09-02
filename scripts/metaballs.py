import bpy
import random
from mathutils import Vector

# Check if script is opened in Blender program
import os, sys
if(bpy.context.space_data == None):
    cwd = os.path.dirname(os.path.abspath(__file__))
else:
    cwd = os.path.dirname(bpy.context.space_data.text.filepath)
# Get folder of script and add current working directory to path
sys.path.append(cwd)
import utils


def createMetaball(origin=(0, 0, 0), n=30, r0=4, r1=2.5):
    metaball = bpy.data.metaballs.new('MetaBall')
    obj = bpy.data.objects.new('MetaBallObject', metaball)
    bpy.context.scene.objects.link(obj)

    metaball.resolution = 0.2
    metaball.render_resolution = 0.05

    for i in range(n):
        location = Vector(origin) + Vector(random.uniform(-r0, r0) for i in range(3))

        element = metaball.elements.new()
        element.co = location
        element.radius = r1

    return metaball


if __name__ == '__main__':
    # Remove all elements
    utils.removeAll()

    # Create camera
    target = utils.target()
    camera = utils.camera((-10, -10, 10), target)

    # Create lamps
    utils.rainbowLights(10, 300, 3)

    # Create metaball
    metaball = createMetaball()

    # Specify folder to save rendering
    render_folder = os.path.join(cwd, 'rendering')
    if(not os.path.exists(render_folder)):
        os.mkdir(render_folder)

    # Render image
    rnd = bpy.data.scenes['Scene'].render
    rnd.resolution_x = 500
    rnd.resolution_y = 500
    rnd.resolution_percentage = 100
    rnd.filepath = os.path.join(render_folder, 'metaballs.png')
    bpy.ops.render.render(write_still=True)
