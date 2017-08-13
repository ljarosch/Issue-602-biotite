# Copyright 2017 Patrick Kunzmann.
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

from os.path import realpath, dirname, join, isdir
from os import listdir, makedirs
from importlib import import_module
import types
import sys
import abc


##### API Doc creation #####

_indent = " " * 4
l = []

def create_api_doc(src_path, doc_path):
    package_list = _create_package_doc("biopython",
                                       join(src_path, "biopython"),
                                       doc_path)
    for p in package_list:
        print(p)


def _create_package_doc(pck, src_path, doc_path):
    if not _is_package(src_path):
        return []
    else:
        content = listdir(src_path)
        dirs = [f for f in content if isdir(join(src_path, f))]
        sub_pck = []
        for directory in dirs:
            sub = _create_package_doc(pck + "." + directory,
                                      join(src_path, directory),
                                      doc_path)
            sub_pck += sub
        
        module = import_module(pck)
        attr_list = dir(module)
        func_list = [attr for attr in attr_list
                     if attr[0] != "_"
                     and type(getattr(module, attr)) == types.FunctionType]
        class_list = [attr for attr in attr_list
                     if attr[0] != "_"
                     and type(getattr(module, attr)) in [type, abc.ABCMeta]]
        _create_files(doc_path, pck, class_list, func_list, sub_pck)
        
        return([pck] + sub_pck)


def _create_files(doc_path, package, classes, functions, subpackages):
    sub_path = join(doc_path, package)
    if not isdir(sub_path):
        makedirs(sub_path)
    
    for cls in classes:
        file_content = \
        """
{:}.{:}
{:}

.. autoclass:: {:}.{:}
    :members:
    :undoc-members:
    :inherited-members:
        """.format(package, cls, "=" * (len(package)+len(cls)+1),
                   package, cls)
        with open(join(sub_path, cls+".rst"), "w") as f:
            f.write(file_content)
            
    for func in functions:
        file_content = \
        """
{:}.{:}
{:}

.. autofunction:: {:}.{:}
        """.format(package, func, "=" * (len(package)+len(func)+1),
                   package, func)
        with open(join(sub_path, func+".rst"), "w") as f:
            f.write(file_content)
    
    
    lines = []
    
    lines.append(package)
    lines.append("=" * len(package))
    lines.append("\n")
    lines.append(".. automodule:: " + package)
    lines.append("\n")
    
    lines.append("Classes")
    lines.append("-" * len("Classes"))
    lines.append("\n")
    for cls in classes:
        lines.append(_indent + "- :doc:`"
                     + package + "." + cls
                     + " <" + package + "/" + cls + ">`")
    lines.append("\n")
    
    lines.append("Functions")
    lines.append("-" * len("Functions"))
    lines.append("\n")
    for func in functions:
        lines.append(_indent + "- :doc:`"
                     + package + "." + func
                     + " <" + package + "/" + func + ">`")
    lines.append("\n")
    
    lines.append("Subpackages")
    lines.append("-" * len("Subpackages"))
    lines.append("\n")
    for pck in subpackages:
        lines.append(_indent + "- :doc:`"
                     + pck
                     + " <" + pck + ">`")
    lines.append("\n")
    
    with open(join(doc_path, package+".rst"), "w") as f:
        f.writelines([line+"\n" for line in lines])


def _is_package(path):
    content = listdir(path)
    return "__init__.py" in content


##### General #####

package_path = join( dirname(dirname(realpath(__file__))), "src" )
sys.path.insert(0, package_path)
create_api_doc(package_path, "apidoc")

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'sphinx.ext.mathjax',
              'sphinx.ext.viewcode',
              'sphinx.ext.autosummary',
              'numpydoc']

templates_path = ['templates']
source_suffix = ['.rst']
master_doc = 'index'

project = 'Biopython'
copyright = '2017, Patrick Kunzmann'
author = 'Patrick Kunzmann'
version = '2.0'
release = '2.0a1'

exclude_patterns = ['build']

pygments_style = 'sphinx'

todo_include_todos = False


##### HTML #####

html_theme = 'nature'
html_static_path = ['static']
htmlhelp_basename = 'BiopythonDoc'


##### LaTeX #####

latex_elements = {}
latex_documents = [
    (master_doc, 'Biopython.tex', 'Biopython Documentation',
     'Patrick Kunzmann', 'manual'),
]

