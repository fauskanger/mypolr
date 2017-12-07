#
# Shared as a gist on:
#   https://gist.github.com/fauskanger/1eff19047f00ebd0a52f1f8698f9f0a7
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Examples on how to use
#
#
# From code:
# my_envs = join('E:\\', 'Anaconda3', 'envs')
# tem = ToxEnvMatcher(my_envs)
# for version in '27,34,35,36'.split(','):
#     tem.make(version)
#
#
# From command line:
# python tox_with_conda.py E:\Anaconda3\envs 27 34 35 36 37
#
from subprocess import run
from os.path import join

from sphinx.addnodes import desc

DEFAULT_BASE = join('C:\\', 'Python')


class ToxEnvMatcher:
    """
    Utility to make conda environments work with tox.

    Conda envs might be in other locations than where `tox <https://tox.readthedocs.io>`_ expects them to be.

    A symbolic link 'Directory Junction' is created from expected location to the actual location.
    Intended for Windows to get around the ``InterpreterNotFound``-error.

    E.g.: tox expects to find Python 2.7 in ``C:\Python27``,
    but may actually be installed in another drive and location.

    Examples of use:

    .. code-block:: python

        my_envs = join('E:\\', 'Anaconda3', 'envs')
        tem = ToxEnvMatcher(my_envs)
        for version in '27,34,35,36'.split(','):
            tem.make(version)

    The class is utilized through ``argsparse`` so it can also be used from cmd.exe.

    Examples of use of th of using ``ToxEnvMatcher`` from cmd.exe:

    .. code-block:: none

        E:\dev> tox_with_conda.py E:\Anaconda3\envs 27 34 35 36 37

    It's possible to use the ``-b``/``--base`` option to override the default base location (``C:\Python``):

    .. code-block:: none

        E:\dev> tox_with_conda.py E:\Anaconda3\envs 27 34 35 36 37 --base D:\Python

    :param str envs_dir: The path to where new conda environments will be created
    :param str default_base: The base of the 'default' location. Usually it's ``C:\Python``
    """
    def __init__(self, envs_dir, default_base=DEFAULT_BASE):
        self.envs_dir = envs_dir
        self.default_base = default_base

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.envs_dir)

    def make(self, version):
        """
        Take version and create conda environment with symlink from 'default tox location'.

        E.g.: given version='27' and environment folder ``{self.envs_dir}``:

         - ``conda create -p {self.envs_dir}\py27 python=2.7``
         - ``mklink /J C:\Python27 {self.envs_dir}\py27``

        :param str version: A string on the form 'XY', e.g. '27' or '36'
        :return: None
        :rtype: NoneType
        """
        if len(version) != 2 or not int(version):
            raise ValueError("Parameter 'version' must be on the form 'XY', and not '{}'".format(version))
        conda_cmd = self._create_cmd_args(version)
        symlink_cmd = self._create_symlink_args(version)
        run(conda_cmd, shell=True)
        run(symlink_cmd, shell=True)

    def _get_env_folder(self, version):
        return join(self.envs_dir, 'py{}'.format(version))

    def _create_cmd_args(self, version):
        env_dir = self._get_env_folder(version)
        python_version = '.'.join(version)
        conda_create = 'conda create -p {} python={} --yes'.format(env_dir, python_version)
        return conda_create.split(' ')

    def _create_symlink_args(self, version):
        env_dir = self._get_env_folder(version)
        return 'mklink /J {}{} {}'.format(self.default_base, version, env_dir).split(' ')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("env_dir",
                        help="The folder where conda environments should be installed.")
    parser.add_argument("versions", nargs='*',
                        help="The list of versions, formatted 'XY' where X is major and Y minor. E.g. '27 35 36'")
    parser.add_argument("-b", "--base", default=DEFAULT_BASE,
                        help="Base of the path which tox expects to find Python installed. "
                             "Default: {}.".format(DEFAULT_BASE))
    args = parser.parse_args()

    print('env_dir: ', args.env_dir)
    print('versions: ', args.versions)
    print('--base: ', args.base)

    tem = ToxEnvMatcher(args.env_dir, default_base=args.base)
    for version in args.versions:
        tem.make(version)
