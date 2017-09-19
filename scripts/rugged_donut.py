import bpy
from math import pi, sin, cos
import utils
import os

# Remove all elements
utils.removeAll()

# Create camera and lamp
utils.simpleScene((0, 0, -0.3), (4.2, 4.2, 5), (-5, 5, 10))

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
bpy.context.scene.objects.link(empty)

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

# Create marble texture for the displace modifier
displacetex = bpy.data.textures.new('Texture', 'MUSGRAVE')
displacetex.musgrave_type = 'RIDGED_MULTIFRACTAL'
displacetex.octaves = 1.5
displacetex.noise_scale = 1.1

# Create and apply displace modifier
displace = obj.modifiers.new('Displace', 'DISPLACE')
displace.texture = displacetex
displace.texture_coords = 'OBJECT'
displace.texture_coords_object = empty
displace.mid_level = 0
displace.strength = 0.6

# Apply subsurf modifier
subsurf = obj.modifiers.new('Subsurf', 'SUBSURF')

# Create bump map texture
bumptex = bpy.data.textures.new('BumpMapTexture', 'CLOUDS')
bumptex.noise_type = 'HARD_NOISE'
bumptex.noise_scale = 0.24
bumptex.noise_depth = 3

# Use some colors
palette = [(105,210,231), (255,152,94)]
# Convert color and apply gamma correction
palette = [tuple(pow(float(c)/255.0, 2.2) for c in color)
            for color in palette]

# Set background color
bpy.context.scene.world.horizon_color = palette[0]

# Create material for the object
mat = bpy.data.materials.new('BumpMapMaterial')
mat.diffuse_color = palette[1]
mat.specular_intensity = 0
mat.emit = 0.1

# Add texture slot for material
slot = mat.texture_slots.add()
slot.texture = bumptex
# Texture mapping: https://docs.blender.org/manual/ko/dev/render/blender_render/textures/properties/mapping.html
slot.texture_coords = 'GLOBAL'
slot.use_map_color_diffuse = False
slot.use_map_normal = True

# Append material to object
obj.data.materials.append(mat)

# Render scene
utils.renderToFolder('frames_01', 'rugged_donut', 800, 800,
    animation=True, frame_end=num_frames)
