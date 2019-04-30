import setuptools
import os

path_to_here = os.path.dirname(os.path.abspath(__file__))
cqc_init = os.path.join(path_to_here, "cqc", "__init__.py")

with open(cqc_init, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith("__version__"):
            version = line.split("__version__ = ")[1]
            version = version.split(' ')[0]
            version = eval(version)
            break
    else:
        raise RuntimeError("Could not find the version!")

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    install_requires = [line.strip() for line in f.readlines()]

setuptools.setup(
    name="cqc",
    version=version,
    author="Axel Dahlberg",
    author_email="e.a.dahlberg@tudelft.nl",
    description="The CQC interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SoftwareQuTech/CQC-Python",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
