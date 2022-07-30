"""Script for setuptools."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

dependencies = [
    "rsa>=4.8"
]

setup(
    name='csck541',
    version='1.0.1',
    author='Zhu Lin Ch\'ng',
    author_email='z.chng@liverpool.ac.uk',
    description='Simple Client-Server Network',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zhulinchng/CSCSK541',
    license='MIT',
    packages=find_packages(),
    install_requires=dependencies,
)
