import os
import sys

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path
    
def read_file(file_name, rmnl=False):
    '''read specified file and remove newlines depend on "rmnl" parameter'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    path = os.path.join(path, file_name)
    try:
        with open(path, "r") as file:
            if rmnl:
                fileContent = file.read().splitlines()
            else:
                fileContent = file.readlines()
    except:
        fileContent = []
    return fileContent

def simple_write(file, list_content):
    '''simple_write data to .txt file, with specified strContent'''
    with open(file, "w") as f:
        for line in list_content:
            try:
                f.write("{}".format(line) + "\n")
            except:
                print('could not write: {}'.format(line))
        f.close()
    return True    
    
if __name__ == "__main__":
    file = "country_list_by_cute_baby_names.txt"
    content = read_file(file, rmnl=True)
    content = list(set([item.split(" in ")[1].split("\t")[0] for item in content if item.strip()]))
    content.sort()
    print(content)
    