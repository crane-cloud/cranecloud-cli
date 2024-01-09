from setuptools import setup, find_packages

setup(
    name='cranecloud',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'create-config=src.cranecloud:create_initial_config',
            'cranecloud=src.cranecloud:cli',
        ],
    },
)
