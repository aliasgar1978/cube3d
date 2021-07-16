import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cube3d",
    version="0.0.1",
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="3-Dimention Rubic cube activities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alias1978/cube3d",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['pandas', 'xlrd', 'numpy'],
)