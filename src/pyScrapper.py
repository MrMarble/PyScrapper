import os
import logging
import json
import pymysql
from pathlib import Path
import shops

CURRENT_PATH = str(Path(os.path.dirname(os.path.realpath(__file__)) + '/').parent)


def set_up():
    try:
        with open(CURRENT_PATH + '/config.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        if type(e) is FileNotFoundError:
            logging.warning('Config file not found.\nCreating basic template...')
        elif type(e) is json.decoder.JSONDecodeError:
            logging.warning('Config file is corrupted!\nCreating a new one...')

        config = dict(dbhost="localhost", dbuser="root", dbpassword="root", dbname="prices")
        json.dump(config, open(CURRENT_PATH + '/config.json', 'w'), indent=True)
        exit(0)


def run(config):
    try:
        db = pymysql.connect(config['dbhost'], config['dbuser'], config['dbpassword'], config['dbname'])
        cursor = db.cursor()
    except (pymysql.err.OperationalError) as e:
        if type(e) is pymysql.err.OperationalError:
            logging.error("Can't connect to MySQL server on '{}'".format(config['dbhost']))


if __name__ == '__main__':
    config = set_up()
    run(config)
