from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Compiler import Options

Options.annotate = True

ext_modules = [
	Extension(
			"LDA_C",
			["LDA.pyx"],
			language="c++",
			extra_compile_args=['-O3']
	)
]

setup(
	cmdclass = {'build_ext': build_ext},
	ext_modules = ext_modules
)

# setup(
# 	cmdclass = {'build_ext': build_ext},
# 	ext_modules = [Extension("LDA_C", ["LDA.pyx"],
# 			include_dirs=[np.get_include()])]
# )