from distutils.core import setup, Extension

setup(name = '_intcode',
      version = '0.1',
      ext_modules = [Extension('_intcode', sources = ['_intcode.c'])])
