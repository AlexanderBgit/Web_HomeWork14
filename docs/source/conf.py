import sys
import os
print(sys.path)

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    from src.config import settings
except Exception as e:
    print(f"Failed to import settings: {e}")
    settings = None

try:
    import src
except ImportError:
    print("Module not found")

sys.path.append(os.path.abspath('..'))


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