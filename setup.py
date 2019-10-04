import setuptools


def read(fname):
    with open(fname, "r") as fh:
        return fh.read()


LONG_DESCRIPTION = read("README.md") + read("CHANGELOG.md")

INSTALL_REQUIRES = [
    "pandas>=0.23.0",
    "numpy>=1.16.0",
    "xarray>=0.13",
    "scipy>=1.3",
    "statsmodels>=0.10",
    "jupyterlab>=1.1",
    "matplotlib>=3.0",
    "dataclasses",
    "ipykernel",
    "jupyter-contrib-nbextensions",
]
EXTRAS_REQUIRE = {
    "tests": ["hypothesis[numpy]", "pytest"],
    "pypi": ["twine"],
    "debug": ["pdbpp"],
    "extra_runtime_libs": ["holidays>=0.9"],
}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"]
    + EXTRAS_REQUIRE["pypi"]  # NOQA
    + EXTRAS_REQUIRE["debug"]  # NOQA
    + EXTRAS_REQUIRE["extra_runtime_libs"]  # NOQA
)


setuptools.setup(
    name="ts-eval",
    version="0.1.0",
    author="Vladimir Shulyak",
    author_email="vladimir@shulyak.net",
    description="Time Series analysis and evaluation tools",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/vshulyak/ts-eval",
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
