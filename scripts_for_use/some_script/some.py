import os
import sys

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

path = script_path()
files = [" ".join([some.capitalize() for some in item.split('.')[0].split("_")[:-1]]) for item in os.listdir() if not "(+)" in item]
print(files)