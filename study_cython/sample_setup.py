from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Compiler import Options
import numpy as np

Options.annotate = True

setup(
	cmdclass = {'build_ext': build_ext},
	ext_modules = [Extension("Sample_dig", ["sample.pyx"],
			language="c++", include_dirs=[np.get_include()])]
)