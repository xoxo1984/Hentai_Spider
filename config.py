# -*- coding: UTF-8 -*-

import argparse, os, configparser
from const import CONFIG_FILE

def get_args(path):
    config = configparser.ConfigParser()
    config_path = os.path.join(path, CONFIG_FILE)
    config.read(config_path)
    parser = argparse.ArgumentParser()

    parser.add_argument('-sd', '--savedir', default=config['ARGS']['SAVEDIR'])
    parser.add_argument('-t', '--thread', default=config['ARGS']['THREAD'], type=int)
    parser.add_argument('-tn', '--trynum', default=config['ARGS']['TRYNUM'], type=int)
    parser.add_argument('-to', '--timeout', default=config['ARGS']['TIMEOUT'], type=int)
    if config['ARGS']['RENAME'].upper() == 'FALSE':
        parser.add_argument('-rn', '--rename', default=False, action="store_true")
    elif config['ARGS']['RENAME'].upper() == 'TRUE':
        parser.add_argument('-rn', '--rename', default=True, action="store_true")
    if config['ARGS']['ORIGINAL_PIC'].upper() == 'FALSE':
        parser.add_argument('-o', '--oripic', default=False, action="store_true")
    elif config['ARGS']['ORIGINAL_PIC'].upper() == 'TRUE':
        parser.add_argument('-o', '--oripic', default=True, action="store_true")
    if config['ARGS']['LOG'].upper() == 'FALSE':
        parser.add_argument('-l', '--log', default=False, action="store_true")
    elif config['ARGS']['LOG'].upper() == 'TRUE':
        parser.add_argument('-l', '--log', default=True, action="store_true")
    if config['ARGS']['CONTINUEDOWNLOAD'].upper() == 'FALSE':
        parser.add_argument('-cd', '--continuedownload', default=False, action="store_true")
    elif config['ARGS']['CONTINUEDOWNLOAD'].upper() == 'TRUE':
        parser.add_argument('-cd', '--continuedownload', default=True, action="store_true")
    parser.add_argument('-u', '--username', default=config['USER']['USERNAME'])
    parser.add_argument('-p', '--password', default=config['USER']['PASSWORD'])

    args = parser.parse_args()
    if args.savedir == '':
        print('there is no savedir in ' + CONFIG_FILE + ', default savedir will be\r\n' +
              path)

    return args