import argparse
from pprint import pprint
from pathlib import Path
from configparser import ConfigParser
import stat

from mypolr import __version__, exceptions, PolrApi, DEFAULT_API_ROOT

ini_header = 'connection'


def make_argparser():
    # Set up arguments
    parser = argparse.ArgumentParser(prog='mypolr', description="Shorten urls with Polr Project's API.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", action="store_true", help="Print version")

    api_group = parser.add_argument_group('API arguments', 'Use these for interacting with the API')

    api_group.add_argument("url", nargs='?', default=None, help="The url to process")
    api_group.add_argument("-s", "--server", default=None, help="Server hosting the API")
    api_group.add_argument("-k", "--key", default=None, help="API_KEY to authenticate against server.")
    api_group.add_argument("--api-root", default=DEFAULT_API_ROOT,
                           help="API endpoint root.")
    api_group.add_argument("-l", "--lookup", action="store_true",
                           help="Perform lookup action instead of shorten action.")

    manage_group = parser.add_argument_group('Manage credentials',
                                             'Use these to save, delete or update "server" and "key" locally.')

    manage_group.add_argument("--save", action="store_true",
                              help="Save credentials for later in ~/.mypolr/config.ini")
    manage_group.add_argument("--clear", action="store_true",
                              help="Clear credentials in ~/.mypolr/config.ini")
    return parser


def make_ini_getter(config):
    def get_ini_value(field, fallback=None):
        return config.get(ini_header, field, fallback=fallback)
    return get_ini_value


def run():
    # config.ini
    config_folder = Path().home() / '.mypolr'
    config_file = config_folder / 'config.ini'

    # Parse arguments
    args = make_argparser().parse_args()

    api_server = args.server
    api_root = args.api_root
    api_key = args.key
    url = args.url

    if args.version:
        print('Version: {}'.format(__version__))
        return

    if args.save:
        if any(value is None for value in [api_server, api_key]):
            print('\nDid not save: Provide at least both SERVER and KEY.\n')
        else:
            # Save api connection values to config file
            config_folder.mkdir(exist_ok=True)
            config_file.touch(stat.S_IRWXU)
            config = ConfigParser()
            config[ini_header] = dict(api_server=api_server, api_key=api_key, api_root=api_root)
            with config_file.open('w') as f:
                config.write(f)
                print('Config file saved: {}'.format(config_file))

    if args.clear:
        if config_file.exists():
            config = ConfigParser()
            config[ini_header] = dict()
            with config_file.open('w') as f:
                config.write(f)
                print('Config file cleared: {}'.format(config_file))

    if config_file.exists():
        config = ConfigParser()
        config.read(config_file)
        ini_value = make_ini_getter(config)
        api_server = api_server or ini_value('api_server')
        api_root = api_root or ini_value('api_root')
        api_key = api_key or ini_value('api_key')

    required_for_api_action = dict(server=api_server, key=api_key, url=url)
    if any(arg is None for arg in required_for_api_action.values()):
        if not any([args.save, args.clear]):
            missing_args = ', '.join(key.upper() for key, value in required_for_api_action.items() if value is None)
            print('Incomplete arguments for API action. Missing: {}'.format(missing_args))
    else:
        print('Processing {}\n'.format(url))
        try:
            api = PolrApi(api_server, api_key, api_root)
            if args.lookup:
                result = api.lookup(url)
                print("Lookup result:\n")
                pprint(result)
            else:
                print('Short url: {}'.format(api.shorten(url)))
        except exceptions.MypolrError as e:
            print(e)


if __name__ == '__main__':
    run()
