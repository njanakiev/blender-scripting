import bpy
from math import pi, sin, cos
import utils
import os


if __name__ == '__main__':
    # Remove all elements
    utils.remove_all()

    # Create camera and lamp
    utils.simple_scene((0, 0, -0.3), (4.2, 4.2, 5), (-5, 5, 10))

    # Set number of frames
    num_frames = 100

    # Create Torus
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 0),
        major_segments=120, minor_segments=50,
        major_radius=1.8, minor_radius=0.5)
    obj = bpy.context.active_object
    bpy.ops.object.shade_smooth()

    # Create Empty to control texture coordinates
    empty = bpy.data.objects.new('Empty', None)
    bpy.context.scene.collection.objects.link(empty)

    # Animate empty with keyframe animation
    # keyframe approach adapted from: http://blenderscripting.blogspot.co.at/2011/05/inspired-by-post-on-ba-it-just-so.html
    for frame in range(1, num_frames):
        t = frame / num_frames
        x = 0.7*cos(2*pi*t) + 1
        y = 0.7*sin(2*pi*t)
        z = 0.4*sin(2*pi*t)
        empty.location = (x, y, z)
        empty.keyframe_insert(data_path="location", index=-1, frame=frame)

    # Change each created keyframe point to linear interpolation
    #for fcurve in empty.animation_data.action.fcurves:
    #    for keyframe in fcurve.keyframe_points:
    #        keyframe.interpolation = 'LINEAR'

    # Apply subsurf modifier
    subsurf = obj.modifiers.new('Subsurf', 'SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    # Create marble texture for the displace modifier
    displace_texture = bpy.data.textures.new('Texture', 'MUSGRAVE')
    displace_texture.musgrave_type = 'RIDGED_MULTIFRACTAL'
    displace_texture.octaves = 1.5
    displace_texture.noise_scale = 1.1

    # Create and apply displace modifier
    displace = obj.modifiers.new('Displace', 'DISPLACE')
    displace.texture = displace_texture
    displace.texture_coords = 'OBJECT'
    displace.texture_coords_object = empty
    displace.mid_level = 0
    displace.strength = 0.6

    # Use some colors
    palette = [(131,175,155,255), (250,105,10,255)]
    # Convert color and apply gamma correction
    palette = [tuple(pow(float(c)/255.0, 2.2) for c in color)
               for color in palette]
    
    # Set background color of scene
    bpy.context.scene.world.use_nodes = False
    bpy.context.scene.world.color = palette[0][:3]
    #bpy.context.scene.world.node_tree.nodes["Background"] \
    #    .inputs[0].default_value = palette[0]

    # Create material for the object
    mat = bpy.data.materials.new('BumpMapMaterial')
    mat.use_nodes = True
    material_node = mat.node_tree.nodes[0]
    material_node.inputs['Base Color'].default_value = palette[1]
    material_node.inputs['Metallic'].default_value = 0.0
    material_node.inputs['Roughness'].default_value = 0.5
    material_node.inputs['Specular'].default_value = 0.5

    # Add bump texture
    bump_texture_node = mat.node_tree.nodes.new('ShaderNodeTexNoise')
    bump_texture_node.noise_dimensions = '3D'
    bump_texture_node.inputs['Scale'].default_value = 20.0
    bump_texture_node.inputs['Detail'].default_value = 4.0
    bump_texture_node.inputs['Roughness'].default_value = 5.0
    
    # Add bump node
    bump_node = mat.node_tree.nodes.new('ShaderNodeBump')
    bump_node.inputs['Strength'].default_value = 0.4
    
    # Link nodes
    mat.node_tree.links.new(
        bump_node.inputs['Height'], bump_texture_node.outputs[0])
    mat.node_tree.links.new(
        material_node.inputs['Normal'], bump_node.outputs[0])

    # Append material to object
    obj.data.materials.append(mat)

    # Render scene
    utils.render('frames_01', 'rugged_donut', 512, 512,
        animation=True,
        render_engine='BLENDER_EEVEE',
        frame_end=num_frames)
