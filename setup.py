from distutils.core import setup

setup(
    name='tubo',
    version='0.1.0',
    author='Antonio Lima',
    author_email='anto87@gmail.com',
    packages=['tubo', 'tubo.test'],
    url='http://pypi.python.org/pypi/Tubo/',
    license='LICENSE.txt',
    description='Tubo is a library that provides a simple pipeline system for Python.',
    long_description=open('README.rst').read(),
    install_requires=[],
)
