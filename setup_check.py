from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='check_run',
    ext_modules=cythonize('apex_yolov5/check_run.py'),
    py_modules=[]
)
