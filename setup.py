import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='botify',
    version='1.0',
    author="Laurent MOULIN",
    author_email="gignops+botify@gmail.com",
    description="A tools to spread function calls to bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lauin/botify",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    install_requires=[
        'redis'
    ],
)
