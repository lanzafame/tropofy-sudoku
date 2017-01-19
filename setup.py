from setuptools import setup, find_packages

requires = [
    'tropofy',
    'pulp'
]

setup(
    name='tropofy-sudoku',
    version='1.0',
    description='This is my fallback plan, cause I dreamt too big the first time :P',
    author='Adrian Lanzafame',
    url='https://github.com/lanzafame/tropofy-sudoku',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
