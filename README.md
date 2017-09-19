# blender-scripting
This is a simple introduction to scripting in [Blender](https://www.blender.org/) with Python.



## Requirements

`Blender 2.5+`

To run the examples, open your favorite console in the example folder, make sure that the Blender executable is an environment variable or in the PATH environment variable in Windows and run the following command. Make sure to edit in [run_blender_script.py](run_blender_script.py) the `scriptFile` variable to the Python script in the [scripts](scripts) folder you want to execute.

```
blender -b -P run_blender_script.py
```

Another option is to open the script in Blender and run [run_blender_script.py](run_blender_script.py) inside Blender, which is a nice way to test and tweak the files and to see and play with the generated result before rendering.



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

This is a more advanced example for using a [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram). The Voronoi diagram is implemented with the module `scipy.spatial` which can be added with [Scipy](https://www.scipy.org/), or can be found in the Python distribution [Anaconda](https://www.continuum.io/downloads). The steps to use Anaconda as the Interpreter in Blender 2.77 are shown in this [solution](http://blender.stackexchange.com/questions/51067/using-anaconda-python-3-in-blender-winx64).

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

This script implements a [Phyllotaxis](https://en.wikipedia.org/wiki/Phyllotaxis) Flower which aranges leaves or the petals according to the [golden angle](https://en.wikipedia.org/wiki/Golden_angle). Additionally The flower is animated by appending an application handler for frame change by

```python
def handler(scene):
	frame = scene.frame_current
	# Create new geometry for new frame

bpy.app.handlers.frame_change_pre.append(handler)
```

In order to render all frames you can run

```python
bpy.ops.render.render(animation=True)
```


The animation is inspired by the mesmerizing sculptures by [John Edmark](http://www.johnedmark.com/).

![Phyllotaxis Flower](/img/phyllotaxis_flower.gif)
