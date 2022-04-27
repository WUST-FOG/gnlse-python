import pkg_resources

from setuptools import find_packages
from setuptools import setup

with open('requirements.txt', 'r') as fh:
    reqs = [str(requirement)
            for requirement in pkg_resources.parse_requirements(fh)]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gnlse',
    version='2.0.0',
    url='https://github.com/WUST-FOG/gnlse-python',
    author='Redman, P., Zatorska, M., Pawlowski, A., Szulc, D., '
           'Majchrowska, S., Tarnowski, K.',
    description='gnlse-python is a Python set of scripts for solving '
                'Generalized Nonlinear Schrodringer Equation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=reqs,
)
