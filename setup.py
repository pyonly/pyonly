import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pyonly",
    version="0.1",
    author="Bennet Meyer",
    description="Create interactive web UIs with Python instead of JavaScript!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://pyonly.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)