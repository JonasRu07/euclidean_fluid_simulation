from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
    long_description = fh.read()
    
VERSION = '0.0.1'

setup_info = dict(
    name='euclidean fluid simulation',
    version=VERSION,
    author='Jonas Ruppert',
    author_email='rpprtjns@gmail.com',
    description='CFD with grid based and predefined Objects to simulate',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/JonasRu07/euclidean_fluid_simulation',
    packages=find_packages(exclude=('test',)),
    python_requires='>=3.6',
    install_requires=[
        'pygame',
        'numpy'
    ],
)

setup(**setup_info)
