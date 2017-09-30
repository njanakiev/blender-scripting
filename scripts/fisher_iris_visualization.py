import bpy
import bmesh
import utils
import numpy as np
from mathutils import Vector, Matrix
from math import pi


def PCA(data, num_components=None):
    # mean center the data
    data -= data.mean(axis=0)
    # calculate the covariance matrix
    R = np.cov(data, rowvar=False)
    # calculate eigenvectors & eigenvalues of the covariance matrix
    # use 'eigh' rather than 'eig' since R is symmetric,
    # the performance gain is substantial
    V, E = np.linalg.eigh(R)
    # sort eigenvalue in decreasing order
    idx = np.argsort(V)[::-1]
    E = E[:,idx]
    # sort eigenvectors according to same index
    V = V[idx]
    # select the first n eigenvectors (n is desired dimension
    # of rescaled data array, or dims_rescaled_data)
    E = E[:, :num_components]
    # carry out the transformation on the data using eigenvectors
    # and return the re-scaled data, eigenvalues, and eigenvectors
    return np.dot(E.T, data.T).T, V, E


def load_iris():
    try:
        # Load Iris dataset from the sklearn.datasets package
        from sklearn import datasets
        from sklearn import decomposition

        # Load Dataset
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        labels = iris.target_names

        # Reduce components by Principal Component Analysis from sklearn
        X = decomposition.PCA(n_components=3).fit_transform(X)
    except ImportError:
        # Load Iris dataset manually
        iris_data = np.genfromtxt(path, dtype='str', delimiter=',')
        X = iris_data[:, :4].astype(dtype=float)
        y = np.ndarray((X.shape[0],), dtype=int)

        # Create target vector y and corresponding labels
        labels, idx = [], 0
        for i, label in enumerate(iris_data[:, 4]):
            if label not in labelsSet:
                labels.append(label); idx += 1
            y[i] = idx - 1

        # Reduce components by implemented Principal Component Analysis
        X = PCA(X, 3)[0]

    return X, y, labels


def createScatter(X, y, size=0.25):
    labels = set(y)
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), \
              (1, 1, 0), (1, 0, 1), (0, 1, 1)]

    # Create a bmesh for each label
    bmList = []
    for label in labels:
        bmList.append(bmesh.new())

    # Iterate through all the vectors and labels
    for x, label in zip(X, y):
        # Use the vector as translation for each point
        T = Matrix.Translation(x)

        if label % 3 == 0:
            bmesh.ops.create_cube(bmList[label],
                size=size, matrix=T)
        elif label % 3 == 1:
            bmesh.ops.create_icosphere(bmList[label],
                diameter=size/2, matrix=T)
        else:
            bmesh.ops.create_cone(bmList[label],
                segments=6, cap_ends=True,
                diameter1=size/2, diameter2=0,
                depth=size, matrix=T)

    objects = []
    for label, color in zip(labels, colors):
        # Create a mesh from the existing bmesh
        mesh = bpy.data.meshes.new('ScatterMesh {}'.format(label))
        bmList[label].to_mesh(mesh)
        bmList[label].free()

        # Create a object with the mesh and link it to the scene
        obj = bpy.data.objects.new('ScatterObject {}'.format(label), mesh)
        bpy.context.scene.objects.link(obj)
        bpy.context.scene.update()

        # Create materials for each bmesh
        mat = bpy.data.materials.new('ScatterMaterial {}'.format(label))
        mat.diffuse_color = color
        mat.diffuse_intensity = 0.5
        mat.specular_intensity = 0.0
        obj.data.materials.append(mat)

        objects.append(obj)

    return objects


if __name__ == '__main__':
    # Remove all elements
    utils.removeAll()

    # Set ambient occlusion
    utils.setAmbientOcclusion()

    # Create camera and lamp
    target, camera, lamp = utils.simpleScene(
        (0, 0, 0), (6, 6, 2), (-5, 5, 10))

    # Make target as parent of camera
    camera.parent = target

    # Set number of frames
    bpy.context.scene.frame_end = 200

    # Animate rotation of target by keyframe animation
    target.rotation_mode = 'AXIS_ANGLE'
    target.rotation_axis_angle = (0, 0, 0, 1)
    target.keyframe_insert(data_path='rotation_axis_angle', index=-1,
        frame=bpy.context.scene.frame_start)
    target.rotation_axis_angle = (2*pi, 0, 0, 1)
    # Set last frame to one frame further to have an animation loop
    target.keyframe_insert(data_path='rotation_axis_angle', index=-1,
        frame=bpy.context.scene.frame_end + 1)

    # Change each created keyframe point to linear interpolation
    for fcurve in target.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'

    X, y, labels = load_iris()

    createScatter(X, y)

    # Create a grid
    bpy.ops.mesh.primitive_grid_add(
        radius=3,
        location=(0, 0, 0),
        x_subdivisions=15,
        y_subdivisions=15)

    grid = bpy.context.active_object

    # Create grid material
    gridMat = bpy.data.materials.new('GridMaterial')
    gridMat.type = 'WIRE'
    gridMat.use_transparency = True
    gridMat.alpha = 0.3

    grid.data.materials.append(gridMat)


    utils.renderToFolder('frames', 'fisher_iris_visualization', 800, 800,
        animation=False)
