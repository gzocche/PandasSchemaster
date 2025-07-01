from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pandasschemaster",  # Changed to match actual package name
    version="1.0.2",
    author="gzocche",  # Add your name
    author_email="gzocche@outlook.com",  # Add your email
    description="Type-safe DataFrame library with schema validation for pandas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gzocche/PandasSchemaster",  # Add your GitHub URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="pandas, dataframe, schema, validation, type-safety",
    entry_points={
        'console_scripts': [
            'pandasschemaster-generate=pandasschemaster.schema_generator:main',
            'pandaschemstart=scripts.pandaschemstart:main',
        ],
    },
)
