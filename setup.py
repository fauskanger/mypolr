# from distutils.core import setup
from setuptools import setup
# To use a consistent encoding across file types
# https://stackoverflow.com/questions/33891373/difference-between-io-open-vs-open-in-python
# from codecs import open
# from os import path

short_description = 'Simple Python package for using the Polr Project REST API.'

# here = path.abspath(path.dirname(__file__))
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

rtd = 'https://mypolr.readthedocs.io'
long_description = 'Read documentation for more info on {}'.format(rtd)

setup(
    name='mypolr',
    packages=['mypolr'],
    url='https://github.com/fauskanger/mypolr',
    license='MIT',
    author='Thomas Fauskanger',
    author_email='',
    keywords='polr project shorturl api',
    description=short_description,
    long_description=long_description,
    install_requires=['requests'],
    python_requires='>=3.3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],

    # Get version from git: https://pypi.python.org/pypi/setuptools_scm
    # version='0.1.0',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
