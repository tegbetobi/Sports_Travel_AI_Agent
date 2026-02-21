from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="SPORTS TRAVEL AGENT",
    version="0.1",
    author="Tobi",
    packages=find_packages(),
    install_requires = requirements,
)
