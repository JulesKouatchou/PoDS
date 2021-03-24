
from distutils.core import setup

setup(
    name='PoDS',
    version='5.0.0',
    author='Jules Kouatchou',
    author_email='Jules.Kouatchou-1@nasa.gov',
    packages=['PoDS', 'PoDS.pysrc', 'PoDS.tools'],
    url='https://modelingguru.nasa.gov/docs/DOC-1582',
    license='LICENSE.txt',
    description='Application to execute in parallel independent serial tasks on multicore clusters.',
    long_description=open('README.txt').read(),
    install_requires=[
       'Python >= 2.6',
    ],
)
