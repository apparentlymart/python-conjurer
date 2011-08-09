from setuptools import setup
from os.path import join, dirname

try:
    long_description = open(join(dirname(__file__), 'README.rst')).read()
except Exception:
    long_description = None

setup(
    name='python-conjurer',
    version='0.1',
    description='Simple mapping between SQLAlchemy results and objects',
    author='Martin Atkins',
    author_email='mart@degeneration.co.uk',

    long_description=long_description,

    packages=['conjurer'],
    provides=['conjurer'],
    requires=['sqlalchemy'],
)
