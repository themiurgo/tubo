try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='tubo',
    version='0.1.1',
    author='Antonio Lima',
    author_email='anto87@gmail.com',
    packages=['tubo', 'tubo.test'],
    url='http://github.com/themiurgo/tubo',
    license='MIT',
    description='A pipeline library for Python that cuts down your boilerplate code.',
    long_description=open('README.rst').read() + "\n\n" + open("HISTORY.rst").read(),
    install_requires=[],
)
