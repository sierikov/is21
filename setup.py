from setuptools import setup

setup(
    name='is21',
    version='1.0',
    py_modules=['is21'],
    install_requires=['Click'],
    entry_points='''
       [console_scripts]
       is21=is21:cli
    '''
)