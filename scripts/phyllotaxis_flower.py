import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix
from math import sqrt, pi, sin, cos
import utils

TAU = 2*pi
# https://en.wikipedia.org/wiki/Golden_angle
GOLDEN_ANGLE = pi*(3 - sqrt(5))


# Get a frame of a vector (tangent, normal and binormal vectors)
# https://en.wikipedia.org/wiki/Frenet%E2%80%93Serret_formulas
def getTNBfromVector(v):
    v = Vector(v)
    N = v.normalized()
    B = N.cross((0, 0, -1))
    if(B.length == 0):
        B, T = Vector((1, 0, 0)), Vector((0, 1, 0))
    else:
        B.normalize()
        T = N.cross(B).normalized()

    return T, N, B


class PhyllotaxisFlower():
    def __init__(self, scene):
        self.n, self.m = 40, 30
        self.r0, self.r1, self.r2 = 10, 2, 2
        self.h0, self.h1 = 10, 3
        self.frames = scene.frame_end - scene.frame_start + 1

        # Calculate and compensate for angle offset for infinite animation
        self.offset = (self.frames * GOLDEN_ANGLE) % TAU
        if self.offset > pi: self.offset -= TAU

        # Create object
        mesh = bpy.data.meshes.new('PhyllotaxisFlower')
        self.obj = bpy.data.objects.new('PhyllotaxisFlower', mesh)

        # Create mesh
        bm = self.geometry()
        bm.to_mesh(mesh)
        mesh.update()
        bm.free()

        # Link object to scene
        scene.collection.objects.link(self.obj)

        # Append new frame change handler to redraw geometry for each frame
        bpy.app.handlers.frame_change_pre.append(self.__frame_change_handler)


    def __frame_change_handler(self, scene, value):
        frame = scene.frame_current
        # Constrain to frame range
        if(frame < 1): frame = 1
        if(frame >= self.frames): frame = self.frames + 1

        mesh = self.obj.data
        bm = self.geometry(frame - 1)
        bm.to_mesh(mesh)
        mesh.update()
        bm.free()


    def geometry(self, frame=0):
        t = frame / self.frames
        Rot = Matrix.Rotation(0.5*pi, 4, 'Y')
        bm = bmesh.new()

        for i in range(self.n):
            t0 = i / self.n
            r0, theta = t0*self.r0, i*GOLDEN_ANGLE - frame*GOLDEN_ANGLE + t*self.offset

            x = r0*cos(theta)
            y = r0*sin(theta)
            z = self.h0/2 - (self.h0 / (self.r0*self.r0))*r0*r0
            p0 = Vector((x, y, z))

            T0, N0, B0 = getTNBfromVector(p0)
            M0 = Matrix([T0, B0, N0]).to_4x4().transposed()

            for j in range(self.m):
                t1 = j / self.m
                t2 = 0.4 + 0.6*t0
                r1, theta = t2*t1*self.r1, j*GOLDEN_ANGLE #- frame*goldenAngle + t*self.offset

                x = r1*cos(theta)
                y = r1*sin(theta)
                z = self.h1 - (self.h1 / (self.r1*self.r1))*r1*r1
                p1 = Vector((x, y, z))
                T1, N1, B1 = getTNBfromVector(p1)
                M1 = Matrix([T1, B1, N1]).to_4x4().transposed()

                p = p0 + (M0 @ p1)
                r2 = t2*t1*self.r2

                T = Matrix.Translation(p)
                bmesh.ops.create_cone(bm,
                    cap_ends=True, segments=6,
                    diameter1=r2, diameter2=r2,
                    depth=0.1*r2, matrix=T @ M0 @ M1 @ Rot)
        return bm


if __name__ == '__main__':
    # Remove all elements
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Creata phyllotaxis flower
    flower = PhyllotaxisFlower(bpy.context.scene)

    # Create camera and lamp
    target = utils.create_target((0, 0, -1.5))
    camera = utils.create_camera((-21.0, -21.0, 12.5), target, 35)
    sun = utils.create_light((-5, 5, 10), 'SUN', target=target)

    # Select colors
    palette = [(3,101,100), (205,179,128)]
    # Convert color and apply gamma correction
    palette = [tuple(pow(float(c)/255, 2.2) for c in color)
                for color in palette]

    # Smooth surface and add subsurf modifier
    utils.set_smooth(flower.obj, 2)

    # Set background color of scene
    bpy.context.scene.world.use_nodes = False
    bpy.context.scene.world.color = palette[0]

    # Set material for object
    mat = utils.create_material(palette[1], roughness=0.8)
    flower.obj.data.materials.append(mat)

    # Render scene
    utils.render(
        'frames_02', 'phyllotaxis_flower', 512, 512,
        render_engine='CYCLES',
        animation=True,
        frame_end=50)
