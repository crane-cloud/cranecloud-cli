from setuptools import setup, find_packages

setup(
    name='cranecloud',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'keyring',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'cranecloud = src.cranecloud:cli',
        ],
    },

)
