"""
This file enables the mypolr package to be run as a module like
``python -m mypolr arg1 arg2 ...`` for practical use from CLI.

Relies on :class:`MypolrCli` in `mypolr/cli.py`.
"""
if __name__ == '__main__':
    from mypolr.cli import MypolrCli
    MypolrCli().run()
