"""Packaging configuration"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lambda-bundler",
    version="0.0.1-b2",
    author="Maurice Borgmeier",
    description="A utility to bundle python code and/or dependencies for deployment to AWS Lambda",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MauriceBrg/lambda_bundler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    extras_require={
        "dev": [
            "pylint==2.5.3",
            "pytest==5.4.3",
            "pytest-cov==2.10.0",
            "setuptools==40.8",
            "twine==3.2.0",
            "wheel==0.34.2"
        ]
    }
)
