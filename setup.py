# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import glob
import sys
import os

# --- source files ---
source_files = ["enet.pyx"]

_enet_files = glob.glob(os.path.join("enet", "*.c"))
if not _enet_files:
    print("You need to download and extract the ENet 1.3 source to enet/")
    print("Download the source from: http://enet.bespin.org/Downloads.html")
    print("See the README for more instructions")
    sys.exit(1)

source_files.extend(_enet_files)

# --- compile-time macros ---
define_macros = [
    ('HAS_POLL', None),
    ('HAS_FCNTL', None),
    ('HAS_MSGHDR_FLAGS', None),
    ('HAS_SOCKLEN_T', None),
]

libraries = []

if sys.platform == 'win32':
    define_macros.append(('WIN32', None))
    libraries.extend(['ws2_32', 'Winmm'])

# On non-macOS platforms, provide reentrant gethostbyname/gethostbyaddr macros
if sys.platform != 'darwin':
    define_macros.extend([('HAS_GETHOSTBYNAME_R', None), ('HAS_GETHOSTBYADDR_R', None)])

# --- compiler flags ---
if sys.platform == 'win32':
    extra_compile_args = ["/O2"]
else:
    extra_compile_args = ["-O3"]

ext_modules = [
    Extension(
        name="enet",
        sources=source_files,
        include_dirs=[os.path.join("enet", "include")],
        define_macros=define_macros,
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        language="c",
    )
]

# --- declare that there's a top-level module named 'enet' (the compiled extension) ---
py_modules = ["enet"]

# --- make sure the stub ends up in sdist and in installed wheel/site-packages ---
# - package_data helps when packaging files that sit next to packages.
# - data_files ensures a top-level file like enet.pyi is installed into site-packages root.
package_data = {"": ["enet.pyi"]} if os.path.isfile("enet.pyi") else {}
data_files = [("", ["enet.pyi"])] if os.path.isfile("enet.pyi") else []

setup(
    name="enet",
    version="0.0.1",
    py_modules=py_modules,
    ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),
    include_package_data=True,   # honors MANIFEST.in when building sdist
    package_data=package_data,
    data_files=data_files,
    zip_safe=False,
)
