# this code was written by chatgpt

from setuptools import setup, Extension
from Cython.Build import cythonize
import glob
import sys
import os

source_files = ["enet.pyx"]

_enet_files = glob.glob(os.path.join("enet", "*.c"))

if not _enet_files:
    print("You need to download and extract the ENet 1.3 source to enet/")
    print("Download the source from: http://enet.bespin.org/Downloads.html")
    print("See the README for more instructions")
    sys.exit(1)

source_files.extend(_enet_files)

define_macros = [
    ('HAS_POLL', None),
    ('HAS_FCNTL', None),
    ('HAS_MSGHDR_FLAGS', None),
    ('HAS_SOCKLEN_T', None)
]

libraries = []

if sys.platform == 'win32':
    define_macros.extend([('WIN32', None)])
    libraries.extend(['ws2_32', 'Winmm'])

if sys.platform != 'darwin':
    define_macros.extend([('HAS_GETHOSTBYNAME_R', None), ('HAS_GETHOSTBYADDR_R', None)])

extra_compile_args = ["-O3"]
if sys.platform == 'win32':
    extra_compile_args = ["/O2"]

ext_modules = [
    Extension(
        "enet",
        sources=source_files,
        include_dirs=[os.path.join("enet", "include")],
        define_macros=define_macros,
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        language="c",
    )
]

setup(
    name="enet",
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': "3"}),
    zip_safe=False,
)
