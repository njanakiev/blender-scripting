import bpy
import os
import sys

# Specify the script to be executed
scriptFile = "modified_torus.py"

if(bpy.context.space_data == None):
    cwd = os.path.dirname(os.path.abspath(__file__))
else:
    cwd = os.path.dirname(bpy.context.space_data.text.filepath)

# Get scripts folder and add it to the search path for modules
filesDir = os.path.join(cwd, "scripts")
sys.path.append(filesDir)

# Compile and execute script file
file = os.path.join(filesDir, scriptFile)
exec(compile(open(file).read(), scriptFile, 'exec'))
