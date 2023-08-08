from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='yolov5 app',
    ext_modules=cythonize(module_list="**.py", exclude='**/__init__.py'),
)
