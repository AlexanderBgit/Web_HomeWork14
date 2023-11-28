import os

def find_src_module(base_path):
    for root, dirs, files in os.walk(base_path):
        if "src" in dirs:
            return os.path.abspath(os.path.join(root, "src"))
    
    return None

project_base_path = r"D:\PyCoreHw\Py\WebHw14"
src_module_path = find_src_module(project_base_path)

if src_module_path:
    print(f"The 'src' module is located at: {src_module_path}")
else:
    print("The 'src' module was not found.")
