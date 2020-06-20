import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lambu",
    version="0.0.1",
    author="Maurice Borgmeier",
    description="A utility to bundle python code and dependencies for deployment in AWS Lambda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MauriceBrg/lambu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    extras_require={
        "dev": [
            "pytest==5.4.3"
        ]
    }
)