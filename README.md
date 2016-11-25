# blender-scripting-intro
This is a simple introduction to scripting in [Blender](https://www.blender.org/) with Python.

## Requirements

`Blender 2.5+`

To run the examples, go with your favorite console to the example folder, make sure that the blender executable is an environment variable or in the PATH environment variable in Windows and run the following command.

```
blender -b -P simple_sphere.py
```

Another option is to open the script in Blender and run the script there which is a nice way to test and tweak the files.  

## Resources

- [Blender Cookbook](https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook)
- [Blender 3D Python Scripting](https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Introduction)
- [Blender Scripting Blog](http://blenderscripting.blogspot.co.at/)

## Utils

[utils.py](examples/utils.py) are some frequently used functions in blender, which will be used in most of the examples.

## Simple Sphere

[simple_sphere.py](examples/simple_sphere.py) Simple rendering of a smooth sphere. First an ico_sphere is added with

```
bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0))
obj = bpy.context.object
```

And to make it a smooth sphere the subdevision surface modifier is added to the object

```
modifier = obj.modifiers.new('Subsurf', 'SUBSURF')
modifier.levels = 2
modifier.render_levels = 2

mesh = obj.data
for p in mesh.polygons:
	p.use_smooth = smooth
```

![Simple Sphere](/img/simple_sphere.png)

## Parametric Torus

[parametric_torus.py](examples/parametric_torus.py) Parametric generation of a torus. The [torus](https://en.wikipedia.org/wiki/Torus) is created with the following parameterization of a grid of the variables u, v

![Torus Formula](/img/torus_formula.png)

where the values u, v are between 0 and 1 and are then mapped to x, y, z coordinates with the parameterization. In the example the function `torusSurface(r0, r1)` returns a surface parameterization function which is then used in `createSurface(surface, n, m)`, which creates the object from n by m vertices.

![Parametric Torus](/img/parametric_torus.png)

## Metaballs

[metaballs.py](examples/metaballs.py) Generate metaballs in Blender inspired by this [tutorial](http://blenderscripting.blogspot.co.at/2012/09/tripping-metaballs-python.html).

![Metaballs](/img/metaballs.png)

## Voronoi landscape

[voronoi_landscape.py](examples/voronoi_landscape.py)

This is a more advanced example for using a [Voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram) in Blender and Python. The Voronoi diagram is implemented with the module `scipy.spatial` which can be added with [Scipy](https://www.scipy.org/)), or can be found in the Python distribution [Anaconda](https://www.continuum.io/downloads). The steps to use Anaconda as the Interpreter in Blender 2.77 are shown in this [solution](http://blender.stackexchange.com/questions/51067/using-anaconda-python-3-in-blender-winx64).

![Voronoi Landscape](/img/vornoi_landscape.png)
