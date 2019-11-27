from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import subprocess


def read_requirements(filename: str):
    with open(filename) as f:
        requirements = f.read().splitlines()
    return requirements


class CustomInstall(install):
    """Installs package with gcc compiler"""
    def run(self):
        subprocess.call(['apt', 'update'])
        install.run(self)


class CustomDevelop(develop):
    """Develop with gcc compiler"""
    def run(self):
        subprocess.call(['apt', 'install', 'build-essential'])
        self.run(self)

setup(
   name='ts_core',
   version='1.0',
   descrition='This package contains source code for time series core',
   author='Sinyakov Gleb',
   packages=find_packages(),
   install_requires=read_requirements('requirements.txt'),
   cmdclass={
       'develop': CustomDevelop,
       'install': CustomInstall
   }
)
