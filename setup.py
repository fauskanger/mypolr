# from distutils.core import setup
import sys
from setuptools import setup
# To use a consistent encoding across file types
# https://stackoverflow.com/questions/33891373/difference-between-io-open-vs-open-in-python
# from codecs import open
# from os import path

short_description = "Package to easily create and manage short links using the " \
                    "`Polr Project <https://polrproject.org>`_'s REST " \
                    "`API <https://docs.polrproject.org/en/latest/developer-guide/api/>`_ that also has CLI support."

# here = path.abspath(path.dirname(__file__))
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

# Workaround until PyPI is able to build README.rst
rtd = 'https://mypolr.readthedocs.io'
long_description = 'Read documentation for more info on {}'.format(rtd)

# Only include pytest-runner if invoked:
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner', 'pytest', 'responses'] if needs_pytest else []


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
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',  # 2.7 or 3.3+
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],

    # Obtains version from git tags with setuptools_scm
    use_scm_version=True,
    setup_requires=['setuptools_scm'] + pytest_runner,
    tests_requires=['pytest', 'responses']
)
