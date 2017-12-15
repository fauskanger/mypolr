from __future__ import print_function

import argparse
from pprint import pprint
from pathlib import Path
from configparser import ConfigParser
import stat

from mypolr import __version__, exceptions, PolrApi, DEFAULT_API_ROOT


def make_argparser():
    # Set up arguments
    parser = argparse.ArgumentParser(prog='mypolr',
                                     description="Interacts with the Polr Project's API.\n\n"
                                                 "User Guide and documentation: https://mypolr.readthedocs.io",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog="NOTE: if configurations are saved, they are stored as plain text on disk, "
                                            "and can be read by anyone with access to the file.")
    parser.add_argument("-v", "--version", action="store_true", help="Print version and exit.")

    parser.add_argument("url", nargs='?', default=None, help="The url to process.")

    api_group = parser.add_argument_group('API server arguments',
                                          'Use these for configure the API. Can be stored locally with --save.')

    api_group.add_argument("-s", "--server", default=None, help="Server hosting the API.")
    api_group.add_argument("-k", "--key", default=None, help="API_KEY to authenticate against server.")
    api_group.add_argument("--api-root", default=DEFAULT_API_ROOT,
                           help="API endpoint root.")

    option_group = parser.add_argument_group('Action options',
                                             'Configure the API action to use.')

    option_group.add_argument("-c", "--custom", default=None,
                              help="Custom short url ending.")
    option_group.add_argument("--secret", action="store_true",
                              help="Set option if using secret url.")
    option_group.add_argument("-l", "--lookup", action="store_true",
                              help="Perform lookup action instead of shorten action.")

    manage_group = parser.add_argument_group('Manage credentials',
                                             'Use these to save, delete or update SERVER, KEY and/or '
                                             'API_ROOT locally in ~/.mypolr/config.ini.')

    manage_group.add_argument("--save", action="store_true",
                              help="Save configuration (including credentials) in plaintext(!).")
    manage_group.add_argument("--clear", action="store_true",
                              help="Clear configuration.")
    return parser


def get_args(arguments=None):
    """This method makes it possible to test the parser independently"""
    return make_argparser().parse_args(arguments)


class MypolrCli:
    def __init__(self, output_stream=None, args_override=None):
        """
        Class used to handle CLI usage with mypolr.

        :param output_stream: Output stream, defaults to sys.stdout.
        :type output_stream: str or None
        :param args_override: To test the MypolrCli class, pass list of arguments to this argument.
        :type args_override: list(str) or None
        """
        # Output stream, defaults to sys.stdout
        self.print_io = output_stream
        # define config.ini
        self.ini_header = 'connection'
        self.config_folder = Path().home() / '.mypolr'
        self.config_file = self.config_folder / 'config.ini'
        # Parse args. Use args_override when testing MypolrCli
        self.args = args = get_args(args_override)
        # Common vars
        self.api_server = args.server
        self.api_root = args.api_root
        self.api_key = args.key
        self.url = args.url

    def run(self):
        if self.args.version:
            print('Version: {}'.format(__version__), file=self.print_io)
            return

        if self.args.save:
            self.save_ini()
        if self.args.clear:
            self.clear_ini()
        if self.config_file.exists():
            self.load_configs_from_ini()
        self.call_api()

    def make_ini_getter(self):
        config = ConfigParser()
        config.read(self.config_file)

        def get_ini_value(field, fallback=None):
            return config.get(self.ini_header, field, fallback=fallback)
        return get_ini_value

    def save_ini(self):
        if any(value is None for value in [self.api_server, self.api_key]):
            print('\nDid not save: Provide at least both SERVER and KEY.\n', file=self.print_io)
        else:
            # Save api connection values to config file
            self.config_folder.mkdir(exist_ok=True)
            self.config_file.touch(stat.S_IRWXU)
            config = ConfigParser()
            config[self.ini_header] = dict(api_server=self.api_server, api_key=self.api_key, api_root=self.api_root)
            with self.config_file.open('w') as f:
                config.write(f)
                print('Config file saved: {}'.format(self.config_file), file=self.print_io)

    def clear_ini(self):
        if self.config_file.exists():
            config = ConfigParser()
            config[self.ini_header] = dict()
            with self.config_file.open('w') as f:
                config.write(f)
                print('Config file cleared: {}'.format(self.config_file), file=self.print_io)
        else:
            print('\nDid not clear: configuration file does not exists.', file=self.print_io)

    def load_configs_from_ini(self):
        ini_value = self.make_ini_getter()
        self.api_server = self.api_server or ini_value('api_server')
        self.api_root = self.api_root or ini_value('api_root')
        self.api_key = self.api_key or ini_value('api_key')

    def call_api_action(self):
        print('Processing {}\n'.format(self.url), file=self.print_io)
        try:
            api = PolrApi(self.api_server, self.api_key, self.api_root)
            if self.args.lookup:
                url, url_key = self.url.rsplit('/', maxsplit=1) if self.args.secret else (self.url, None)
                result = api.lookup(url, url_key)
                print("Lookup result:\n", file=self.print_io)
                pprint(result, stream=self.print_io)
            else:
                print('Short url: {}'.format(api.shorten(
                    self.url,
                    custom_ending=self.args.custom,
                    is_secret=self.args.secret)
                ), file=self.print_io)
        except exceptions.MypolrError as e:
            print(e, file=self.print_io)

    def call_api(self):
        required_for_api_action = dict(server=self.api_server, key=self.api_key, url=self.url)
        if any(arg is None for arg in required_for_api_action.values()):
            if not any([self.args.save, self.args.clear]):
                missing_args = ', '.join(key.upper() for key, value in required_for_api_action.items() if value is None)
                print('Incomplete arguments for API action. Missing: {}'.format(missing_args), file=self.print_io)
        else:
            self.call_api_action()


if __name__ == '__main__':
    MypolrCli().run()
