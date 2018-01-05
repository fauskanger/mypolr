"""
This file enables the mypolr package to be run as a module like
``python -m mypolr arg1 arg2 ...`` for practical use from CLI.

Relies on :class:`MypolrCli` in `mypolr/cli.py`.
"""
from __future__ import print_function


if __name__ == '__main__':
    from mypolr import is_cli_supported

    if is_cli_supported:
        from mypolr.cli import MypolrCli
        MypolrCli().run()
    else:
        print('\nCLI-usage of mypolr requires Python 3.3 or newer. Sorry.')
        print('Please feel free to add a Pull Request with increased support.')
