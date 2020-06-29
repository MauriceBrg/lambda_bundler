# Lambda Bundler

![Lambda-Bundler-Build](https://github.com/MauriceBrg/lambda_bundler/workflows/Lambda-Bundler-Build/badge.svg?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/d8e6323930db603aad30/maintainability)](https://codeclimate.com/github/MauriceBrg/lambda_bundler/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d8e6323930db603aad30/test_coverage)](https://codeclimate.com/github/MauriceBrg/lambda_bundler/test_coverage)
[![PyPI version](https://badge.fury.io/py/lambda-bundler.svg)](https://badge.fury.io/py/lambda-bundler)

Lambda Bundler helps you package your python lambda functions and their dependencies for deployment to AWS.

It supports three different modes:

- Package dependencies for a Lambda layer
- Package code-only dependencies from multiple directories for deployment to Lambda
- Package your own code and external dependencies into a single zip for deployment to Lambda

Dependencies will be cached if possible in order to provide a fast build experience.

## Installation

The installation is very simple using pip:

```text
pip install lambda-bundler
```

## How to use

### Package a Lambda layer

```python
from lambda_bundler import build_layer_package

path_to_deployment_artifact = build_layer_package(
    # You can install the dependencies from multiple
    # requirement files into a single layer
    requirement_files=[
        "path/to/requirements.txt"
    ]
)

# path_to_deployment_artifact now points to a zip archive with the dependencies.
```

### Package code directories

```python
from lambda_bundler import build_lambda_package

path_to_deployment_artifact = build_lambda_package(
    code_directories=[
        "path/to/package",
        "path/to/other/package
    ],
    exclude_patterns=[
        "*.pyc"
    ]
)

# path_to_deployment_artifact now contains the path to the zip archive
```

### Package code directories and dependencies

If you'd like to package your dependencies directly into the deployment artifact you can do that very easily. Please keep in mind, that the size limit for a zipped deployment package is 50MB according to the [documentation](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html) and the content of packages larger than 3MB won't be visible in the code editor in the console.

```python
from lambda_bundler import build_lambda_package

path_to_deployment_artifact = build_lambda_package(
    code_directories=[
        "path/to/package",
        "path/to/other/package
    ],
    requirement_files=[
        "path/to/requirements.txt
    ],
    exclude_patterns=[
        "*.pyc"
    ]
)

# path_to_deployment_artifact now contains the path to the zip archive
```

## Configuration

The library uses a working directory to build and cache packages.
By default this is located in the `lambda_bundler_builds` folder in your temporary directory as determined by [python](https://docs.python.org/3/library/tempfile.html#tempfile.gettempdir).

If you'd like to change that, you can set the `LAMBDA_BUNDLER_BUILD_DIR` environment variable and point it to another directory.

## Known Limitations

- Packages are downloaded and built on your local machine, that means you might experience problems with libraries that use C-extensions if your platform is not Linux. Building packages with Docker is something I'd like to look into if there's a demand for that.
- Currently there's no warnings/errors if your deployment package surpasses the Lambda limits - if there's a need for that I'll consider adding those.
- This is built towards integration with the AWS CDK in python and doesn't work well standalone. I'm considering adding a CLI interface for use in Deployment Pipelines. Let me know if this is something you could use.