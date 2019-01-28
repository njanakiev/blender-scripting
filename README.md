# blender-scripting
This is a collection of simple to more involved examples to scripting in [Blender](https://www.blender.org/) with Python.



## Table of Contents
- [Requirements](#requirements)
- [Resources](#resources)
- [Utils](#utils)
- [Simple Sphere](#simple-sphere)
- [Parametric Torus](#parametric-torus)
- [Metaballs](#metaballs)
- [Voronoi Landscape](#voronoi-landscape)
- [Tetrahedron Fractal](#tetrahedron-fractal)
- [Phyllotaxis Flower](#phyllotaxis-flower)
- [Rugged Donut](#rugged-donut)
- [Fisher Iris Visualization](#fisher-iris-visualization)
- [Voronoi Sphere](#voronoi-sphere)


## Requirements

`Blender 2.5+`

To run the examples, open your favorite console in the example folder, make sure that the Blender executable is an environment variable or in the PATH environment variable in Windows and run the following command. Make sure to edit in [run_script.py](run_script.py) the `scriptFile` variable to the Python script in the [scripts](scripts) folder you want to execute.

```
blender -b -P run_script.py
```

Another option is to open the script in Blender and run [run_script.py](run_script.py) inside Blender, which is a nice way to test and tweak the files and to see and play with the generated result before rendering.



## Resources

- [Blender Cookbook](https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook)
- [Blender 3D Python Scripting](https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Introduction)
- [Blender Scripting Blog](http://blenderscripting.blogspot.co.at/)



## Utils

[utils](scripts/utils/__init__.py) 

Some frequently used functions in blender, which will be used in most of the scripts.



## Simple Sphere

[simple_sphere.py](scripts/simple_sphere.py) 

Simple rendering of a smooth sphere. First an icosphere is added with

```python
import bpy
bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0))
obj = bpy.context.object
```

Then the subdivision surface modifier is added to the object to increase the resolution of the mesh and afterwards all the faces of the object are set to a smooth shading

```python
modifier = obj.modifiers.new('Subsurf', 'SUBSURF')
modifier.levels = 2
modifier.render_levels = 2

mesh = obj.data
for p in mesh.polygons:
	p.use_smooth = True
```

Alternatively the icosphere can be subdivided with the `subdivisions` argument in the function

```python
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, location=(0, 0, 0))
```

![Simple Sphere](/img/simple_sphere.png)



## Parametric Torus

[parametric_torus.py](scripts/parametric_torus.py) 

Parametric generation of a torus. The [torus](https://en.wikipedia.org/wiki/Torus) is created with the following parameterization of a grid of the variables u, v

![Torus Formula](/img/torus_formula.png)

where the values u, v are between 0 and 1 and are then mapped to x, y, z coordinates. In [parametric_torus.py](scripts/parametric_torus.py), the function `torusSurface(r0, r1)` returns the surface parameterization function for a torus which is then used in `createSurface(surface, n, m)` as the first argument, which creates the object from a n by m grid. The function `createSurface(surface, n, m)` can be also used for other parameterizations such as [surfaces of revolution](https://en.wikipedia.org/wiki/Surface_of_revolution) or other [parametric surfaces](https://en.wikipedia.org/wiki/Parametric_surface).

![Parametric Torus](/img/parametric_torus.png)



## Metaballs

[metaballs.py](scripts/metaballs.py) 

Generate random metaballs in Blender inspired by this [tutorial](http://blenderscripting.blogspot.co.at/2012/09/tripping-metaballs-python.html).

![Metaballs](/img/metaballs.png)



## Voronoi Landscape

[voronoi_landscape.py](scripts/voronoi_landscape.py)

This is a more advanced example for using a [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram). The Voronoi diagram is implemented with the module `scipy.spatial` which can be added with [Scipy](https://www.scipy.org/), or can be found in the Python distribution [Anaconda](https://www.continuum.io/downloads). The steps to use Anaconda as the Interpreter in Blender 2.77 are shown in this [solution](http://til.janakiev.com/using-anaconda-in-blender/).

![Voronoi Landscape](/img/vornoi_landscape.png)



## Tetrahedron Fractal

[tetrahedron_fractal.py](scripts/tetrahedron_fractal.py)

This is an example for a fractal [tetrahedron](http://mathworld.wolfram.com/RegularTetrahedron.html), where each tetrahedron is subdivided into smaller pieces with a recursive function. In order to create a material for the tetrahedron the material is assigned as shown here:

```python
color = (0.5, 0.5, 0.5)
mat = bpy.data.materials.new('Material')
	
# Diffuse
mat.diffuse_shader = 'LAMBERT'
mat.diffuse_intensity = 0.9
mat.diffuse_color = color
	
# Specular
mat.specular_intensity = 0

obj.data.materials.append(mat)
```

![Tetrahedron Fractal](/img/tetrahedron_fractal.png)



## Phyllotaxis Flower

[phyllotaxis_flower.py](scripts/phyllotaxis_flower.py)

This script implements a [Phyllotaxis](https://en.wikipedia.org/wiki/Phyllotaxis) Flower which aranges leaves or the petals according to the [golden angle](https://en.wikipedia.org/wiki/Golden_angle). Additionally The flower is animated by appending an [application handler](https://docs.blender.org/api/blender_python_api_current/bpy.app.handlers.html) for frame change by

```python
def handler(scene):
    frame = scene.frame_current
    # Create new geometry for new frame
    # ...
	
# Append frame change handler on frame change for playback and rendering (before)
bpy.app.handlers.frame_change_pre.append(handler)
```

In order to render all frames you can run

```python
bpy.ops.render.render(animation=True)
```


The animation is inspired by the mesmerizing sculptures by [John Edmark](http://www.johnedmark.com/).

![Phyllotaxis Flower](/img/phyllotaxis_flower.gif)



## Rugged Donut

[rugged_donut.py](scripts/rugged_donut.py)

This script implements a number of different things available in Blender. For one it applies a [Displace modifier](https://docs.blender.org/manual/de/dev/modeling/modifiers/deform/displace.html) to a torus which displaces the object with a texture as follows.

```python
# Create musgrave texture 
texture = bpy.data.textures.new('Texture', 'MUSGRAVE')

# Create displace modifier and apply texture
displace = obj.modifiers.new('Displace', 'DISPLACE')
displace.texture = texture
```

Further we can control the texture by an object such as an [Empty object](https://docs.blender.org/manual/ja/dev/modeling/empties.html)

```python
# Create Empty to control texture coordinates
empty = bpy.data.objects.new('Empty', None)
bpy.context.scene.objects.link(empty)

# Take the texture coordinates from empty’s coordinate system 
displace.texture_coords = 'OBJECT'
displace.texture_coords_object = empty
```

Additionally we want to add a material with additional bump map to our torus object which is done in the following way.

```python
# Create bump map texture
bumptex = bpy.data.textures.new('BumpMapTexture', 'CLOUDS')

# Create material
mat = bpy.data.materials.new('BumpMapMaterial')

# Add texture slot for material and add texture to this slot
slot = mat.texture_slots.add()
slot.texture = bumptex
slot.texture_coords = 'GLOBAL'
slot.use_map_color_diffuse = False
slot.use_map_normal = True

# Append material to object
obj.data.materials.append(mat)
```

Now we want to animate the empty in order to animate the texture. We can achieve this by inserting keyframes for the location of our empty as shown in this quick [tutorial](blenderscripting.blogspot.co.at/2011/05/inspired-by-post-on-ba-it-just-so.html) and in the next snippet.

```python
for frame in range(1, num_frames):
    t = frame / num_frames
    x = 0.7*cos(2*pi*t)
    y = 0.7*sin(2*pi*t)
    z = 0.4*sin(2*pi*t)
    empty.location = (x, y, z)
    empty.keyframe_insert(data_path="location", index=-1, frame=frame)
```

![Rugged Donut](/img/rugged_donut.gif)



## Fisher Iris Visualization

[fisher_iris_visualization.py](scripts/fisher_iris_visualization.py)

This script implements a visualization of the famous [Fisher's Iris data set](https://en.wikipedia.org/wiki/Iris_flower_data_set). The data set consists of 50 samples for each of three flower species of Iris setosa, Iris virginica and Iris versicolor. Each sample consists of four features (sepal length, sepal width, petal length and petal width). In order to visualize the data set in three dimensions we apply dimensionality reduction by using [Principal Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis). The data set and PCA are both included in the [scikit-learn](http://scikit-learn.org/stable/) library for Python. This script works both with or without sklearn which is not part of the Blender Python distribution. You can use sklearn by using [Anaconda](https://anaconda.org/) in Blender which I show in this quick [tutorial](http://til.janakiev.com/using-anaconda-in-blender/).

```python
from sklearn import datasets
from sklearn import decomposition

# Load Dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target
labels = iris.target_names

# Reduce components by Principal Component Analysis from sklearn
X = decomposition.PCA(n_components=3).fit_transform(X)
```
The data set in [/scripts/data/iris/](/scripts/data/iris/) is downloaded from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/iris) and PCA is implemented manually with the help of the included [Numpy](http://www.numpy.org/) library. If sklearn is not in the current Python distribution the Iris data set is loaded as in the next code snippet.

```python
path = os.path.join('data', 'iris', 'iris.data')
iris_data = np.genfromtxt(path, dtype='str', delimiter=',')
X = iris_data[:, :4].astype(dtype=float)
y = np.ndarray((X.shape[0],), dtype=int)

# Create target vector y and corresponding labels
labels, idx = [], 0
for i, label in enumerate(iris_data[:, 4]):
    if label not in labels:
        labels.append(label); idx += 1
    y[i] = idx - 1

# Reduce components by implemented Principal Component Analysis
X = PCA(X, 3)[0]
```

The data set is loaded into the scene as a 3D scatter plot with different shape primitives for each class of flower from the [BMesh Operators](https://docs.blender.org/api/blender_python_api_current/bmesh.ops.html). Additionally each collection of shapes in a class has different materials assigned to them. Each class has corresponding labels which are rotated toward the camera by a [Locked Track Constraint](https://docs.blender.org/manual/en/dev/rigging/constraints/tracking/locked_track.html).

![Fisher Iris Visualization](/img/fisher_iris_visualization.gif)



## Voronoi Sphere

[voronoi_sphere.py](scripts/voronoi_sphere.py)

This is another example using the [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram), but this time in the 3rd dimension. It is implemented as well with the module `scipy.spatial` which can be added with [Scipy](https://www.scipy.org/) and it is even used in a similar way as the previous Voronoi example in 2D.

![Voronoi Sphere](/img/voronoi_sphere.png)
