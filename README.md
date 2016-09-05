# blender-scripting-intro
This is a simple introduction to scripting in [Blender](https://www.blender.org/) with Python.

## Requirements

- `blender 2.5+`

To run the examples, go with your favorite console to the example folder, make sure that the blender executable is an environment variable or in the PATH environment variable in Windows and run the following command.

```
blender -b -P simple_sphere.py
```

Another option is to open the script in Blender and run the script there which is a nice way to test and tweak the files.  

## Resources

- [Blender Cookbook](https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook)
- [Blender 3D Python Scripting](https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Introduction)

## Simple Sphere

![Simple Sphere](/img/simple_sphere.png)

## Parametric Torus

The [torus](https://en.wikipedia.org/wiki/Torus) is created with the following parameterization 

![Torus Formula](/img/torus_formula.png)

This is done by creating a grid of u, v values between 0 and 1

![Parametric Torus](/img/parametric_torus.png)