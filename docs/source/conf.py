import sys
import os

try:
    from src.config import settings
except Exception as e:
    print(f"Failed to import settings: {e}")
    settings = None

try:
    import src
except ImportError:
    print("Module not found")

try:
    from src.config import settings
except ImportError:
    print("Failed: No module named 'src'")
    settings = None

# sys.path.append(os.path.abspath(".."))
# sys.path.insert(0, os.path.abspath('../../src'))
# 
# sys.path.insert(0, 
# # os.path.abspath(os.path.join('..', 'src')))
# 
# sys.path.insert(0, 
# # os.path.abspath(os.path.join('..', '..', 'src')))
# 
# sys.path.insert(0, 
# os.path.abspath(os.path.join('..', '..')))
# 
# sys.path.insert(0, os.path.abspath('../..'))
# 
# sys.path.insert(0, 
# os.path.abspath(os.path.join('D:', 
# 'PyCoreHw', 'Py', 'WebHw14', 'src')))
sys.path.insert(0, 
        os.path.abspath(r'D:\PyCoreHw\Py\WebHw14\src'))

project = 'Rest API 14.0'
copyright = '2023, Borovyk O.'
author = 'Borovyk O.'
release = 'first release'

# autodoc_mock_imports = ['src.config']

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build',
                     'Thumbs.db',
                     '.DS_Store']

language = 'English'


html_theme = 'nature'
html_static_path = ['_static']