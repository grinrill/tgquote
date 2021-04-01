#!/usr/bin/env python3
import pathlib
import re
import sys

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent

# Check python version
# MINIMAL_PY_VERSION = (3, 7)
# if sys.version_info < MINIMAL_PY_VERSION:
#     raise RuntimeError('aiogram works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


def get_version():
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'tgquote' / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def get_description():
    """
    Read full description from 'README.rst'
    :return: description
    :rtype: str
    """
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='tgquote',
    version=get_version(),
    packages=find_packages(exclude=('debug', 'debug.*', 'examples.*', 'docs',)),
    url='https://github.com/grinrill/telegramimage',
    license='MIT',
    author='Grinrill',
    requires_python='>=3.7',
    author_email='kiralgrin@gmail.com',
    description='Is a pretty simple and fully asynchronous framework for quoting telegram messages',
    long_description=get_description(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[],
    extras_require={
        'httpapi': [
	        'aiohttp>=3.7.2,<4.0.0'
        ],
        'pyppeteer': [
        	'pyppeteer>=0.2.5'
        ],
    },
    package_data={
    	'': ['*.jinja2', '*.js', '*.css']
    },
    include_package_data=True,
)