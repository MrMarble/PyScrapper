import os, sys
import logging
import requests
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

        config = dict(db_type="sqlite", db_host="localhost", db_user="root", db_password="root", db_name="prices", tg_token="BOT_TOKEN", tg_chat_id="000000000")
        json.dump(config, open(CURRENT_PATH + '/config.json', 'w'), indent=True)
        exit(0)


def run(_config):
    logging.basicConfig(level=logging.INFO, filename=CURRENT_PATH + '/log.txt', format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    logging.info('Connecting to the database')

    db = database.database(_config['db_type'], _config['db_host'], _config['db_user'], _config['db_password'], _config['db_name'])
    
    logging.info('Connected!')
    logging.info('Getting products...')

    _products = db.get_products()

    logging.info('{} Products obtained from the database'.format(len(_products)))

    for product in _products:
        logging.info('Fetching price for product ID: {}'.format(product.id))

        current_product = None

        if product.shop == 'Amazon':
            current_product = shops.Amazon(product.id, product.url)
        elif product.shop == 'fnac':
            current_product = shops.Fnac(product.id, product.url)
        elif product.shop == 'MediaMarkt':
            current_product = shops.MediaMarkt(product.id, product.url)

        if db.is_cheapest( current_product.id, current_product.price ) and current_product is not None:
            logging.info('The product with ID: {} is cheaper'.format(product.id))
            requests.get('https://api.telegram.org/bot{}/sendmessage?text={}&chat_id={}'.format(_config['tg_token'], 'El producto {} esta mas barato. {}€'.format(product.name, current_product.price), _config['tg_chat_id']))

        if current_product is not None:
            db.insert_price(current_product.id, current_product.price)
        
            
    logging.info('All Done!')


if __name__ == '__main__':
    config = set_up()
    run(config)
