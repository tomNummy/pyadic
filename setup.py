from setuptools import find_packages, setup

setup(
    name="pyadic",
    author="tomNummy",
    author_email="tom.nummy@gmail.com",
    description="Tools for analyzing chat transcripts",
    url="https://github.com/tomNummy/pyadic",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["networkx", "click", "pydantic", "bokeh"],
    license="MIT License",
)
