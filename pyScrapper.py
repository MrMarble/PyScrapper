import os
import logging
import json
import database
import shops

CURRENT_PATH = (os.path.dirname(os.path.realpath(__file__)) + '/')


def set_up():
    try:
        with open(CURRENT_PATH + '/config.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        if type(e) is FileNotFoundError:
            logging.warning('Config file not found.\nCreating basic template...')
        elif type(e) is json.decoder.JSONDecodeError:
            logging.warning('Config file is corrupted!\nCreating a new one...')

        config = dict(db_type="sqlite", db_host="localhost", db_user="root", db_password="root", db_name="prices")
        json.dump(config, open(CURRENT_PATH + '/config.json', 'w'), indent=True)
        exit(0)


def run(_config):
    logging.basicConfig(level=logging.INFO, filename=CURRENT_PATH + '/log.txt', format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
    logging.info('Connecting to the database')

    db = database.database(_config['db_type'], _config['db_host'], _config['db_user'], _config['db_password'], _config['db_name'])
    
    logging.info('Connected!')
    logging.info('Getting products...')

    _products = db.get_products()

    logging.info('{} Products obtained from the database'.format(len(_products)))

    for product in _products:
        logging.info('Fetching price for product ID: {}'.format(product[0]))

        p = None
        if product[1] == 'Amazon':
            p = shops.Amazon(product[0], product[2])
        elif product[1] == 'fnac':
            p = shops.Fnac(product[0], product[2])
        elif product[1] == 'MediaMarkt':
            p = shops.MediaMarkt(product[0], product[2])
        if p is not None:
            db.insert_price(p.id, p.price)
            
    logging.info('All Done!')


if __name__ == '__main__':
    config = set_up()
    run(config)
