# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.


from setuptools import find_namespace_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("src/braket/qrack_simulator/_version.py") as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")


setup(
    name="amazon-braket-qrack-cpu-simulator",
    version=version,
    license="Apache License 2.0",
    python_requires=">= 3.9",
    packages=find_namespace_packages(where="src", exclude=("test",)),
    package_dir={"": "src"},
    package_data={"": ["*.g4", "*.inc"]},
    include_package_data=True,
    install_requires=[
        "pyqrack-cpu>=1.27.0",
        "qiskit",
        "qiskit_qasm3_import",
        "amazon-braket-sdk",
    ],
    entry_points={
        "braket.simulators": [
            "qrack = braket.qrack_simulator.qrack_simulator:BraketQrackSimulator",
        ]
    },
    extras_require={
        "test": [
            "black",
            "flake8",
            "flake8-rst-docstrings",
            "isort",
            "pre-commit",
            "pylint",
            "pytest==7.2.0",
            "pytest-benchmark",
            "pytest-cov",
            "pytest-rerunfailures",
            "pytest-xdist",
            "sphinx",
            "sphinx-rtd-theme",
            "sphinxcontrib-apidoc",
            "tox",
        ]
    },
    url="https://github.com/amazon-braket/amazon-braket-qrack-simulator-python",
    author="Unitary Fund, Amazon Web Services",
    description=(
        "An open source quantum circuit simulator to be run locally with the Amazon Braket SDK"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Qrack Amazon AWS Quantum",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
