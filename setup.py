"""Manage dependencies."""
import pathlib
from typing import List
from setuptools import find_packages, setup


def _read(fname: str) -> str:
    with open(pathlib.Path(fname)) as fh:
        data = fh.read()
    return data


base_packages: List[str] = ["rply"]

dev_packages = [
    "black",
    "ipykernel",
    "isort",
    "pre-commit",
]


test_packages = [
    "pytest",
]


setup(
    name="pascal_like_interpreter",
    version="0.0.1",
    packages=find_packages(exclude=["notebooks", "tests"]),
    long_description=_read("README.md"),
    install_requires=base_packages,
    extras_require={
        "dev": dev_packages + test_packages,
        "test": test_packages,
    },
)
