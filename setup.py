from io import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='shared',
    version='0.1.1',
    description='Shared functionality for CIS functionality',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nichigas/cis_ng-shared',
    author='Codeborne',

    keywords='python',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.6',
    install_requires=[
        'apispec',
        'flask_apispec',
        'flask_jwt_extended',
        'marshmallow',
        'simplejson',
        'flask',
        'requests',
        'marshmallow_enum',
        'PyMySQL',
        'pytz',
        'sqlalchemy',
        'json_log_formatter',
        'pytest',
        'pika'
    ]
)
