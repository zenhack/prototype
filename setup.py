from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')

setup(name='sterling',
      version='0.1',
      author='Ian Denhardt',
      author_email='ian@zenhack.net',
      url='https://github.com/sterling-ui/prototype',
      packages=find_packages(),
      requires=[str(r.req) for r in install_reqs],
     )
