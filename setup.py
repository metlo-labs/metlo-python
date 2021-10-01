import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

with open(this_directory / 'requirements.in') as f:
    required = f.read().strip().splitlines()

setuptools.setup(
    name='metlo',
    version='0.0.11',
    author='S2 Labs Inc.',
    author_email='akshay@metlo.com',
    description='Metlo\'s Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.0',
    license="MIT",
    entry_points = {
        'console_scripts': ['metlo=metlo.command_line:main'],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    project_urls={
        'Homepage': 'https://www.metlo.com',
        'Documentation': 'https://docs.metlo.com',
        'Source Code': 'https://github.com/metlo-labs/metlo-python',
    },
    py_modules=['metlo'],
    package_dir={'':'.'},
    install_requires=required,
)
