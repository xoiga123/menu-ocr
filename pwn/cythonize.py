from distutils.core import setup
from Cython.Build import cythonize

setup(
    name= 'lmao',
    ext_modules = cythonize("final_processing.pyx")
)