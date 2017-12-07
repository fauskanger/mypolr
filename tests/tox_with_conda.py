#   Source:
#       https://github.com/fauskanger/tox_with_conda
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

# The location where tox expects python to be installed.
# E.g. C:\Python27 or C:\Python35
DEFAULT_BASE = join('C:\\', 'Python')

# The prefix for names of newly created conda environments.
# E.g. py27 or py35 in E:\Anaconda3\envs
DEFAULT_ENV_PREFIX = 'py'


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
    def __init__(self, envs_dir, default_base=DEFAULT_BASE, env_prefix=DEFAULT_ENV_PREFIX):
        self.envs_dir = envs_dir
        self.default_base = default_base
        self.env_prefix = env_prefix

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
        """
        Given version, return the folder in which a new conda environment is created.

        :param str version: A string on the form 'XY', e.g. '27' or '36'
        :return: The path to the new environment, e.g.: *E:\Anaconda3\envs\py27*
        :rtype: str
        """
        return join(self.envs_dir, '{}{}'.format(self.env_prefix, version))

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

    parser = argparse.ArgumentParser(description="Will create conda environements in the <env_dir> for each version "
                                                 "of the <versions>. "
                                                 "Each environment will be create on the form "
                                                 "<env_dir>\\<env_prefix><version> and "
                                                 "have a 'Directory Juntion' symbolic link made from "
                                                 "<base><version>.")
    parser.add_argument("env_dir",
                        help="The folder where conda environments should be installed.")
    parser.add_argument("versions", nargs='*',
                        help="The list of versions, formatted 'XY' where X is major and Y minor. E.g. '27 35 36'")
    parser.add_argument("-b", "--base", default=DEFAULT_BASE,
                        help="Base of the path which tox expects to find Python installed. "
                             "Default: {}.".format(DEFAULT_BASE))
    parser.add_argument("-p", "--env_prefix", default=DEFAULT_ENV_PREFIX,
                        help="Prefix to add before the version in newly created environments. "
                             "Default: {}.".format(DEFAULT_ENV_PREFIX))
    args = parser.parse_args()

    print('env_dir: ', args.env_dir)
    print('env_prefix: ', args.env_prefix)
    print('versions: ', args.versions)
    print('--base: ', args.base)

    tem = ToxEnvMatcher(args.env_dir, default_base=args.base, env_prefix=args.env_prefix)
    for version in args.versions:
        tem.make(version)
