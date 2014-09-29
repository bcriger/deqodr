from distutils.core import setup

#The only reason this is here is to make sure that QuaEC is installed
#automatically.
setup(
    name='deqodr',
    version='0.0.0',
    author='Ben Criger',
    author_email='bcriger@gmail.com',
    package_dir={'': 'src'},
    packages=['deqodr'],
    requires=['numpy', 'qecc']
)
