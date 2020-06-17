import os, sys, re
import logging
import json
import database
import shops
import notifications

CURRENT_PATH = (os.path.dirname(os.path.realpath(__file__)) + '/')


def set_up():
    try:
        if not os.path.exists(CURRENT_PATH + 'urls.csv'):
            with open(CURRENT_PATH + 'urls.csv', 'w') as f:
                f.write('name,url')

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

    logging.info('Reading file urls')
    try:
        with open('urls.csv') as f:
            urls = [line.rstrip() for line in f]
    
        for url in urls:
            data = url.split(',')

            if url == "" or data[1].strip() == "url":
                continue

            db.insert_products(data[0].strip(),data[1].strip(),re.search(R'[\w\d]*\.([\w\d]+)\.\w{2,3}/', data[1]).group(1))
        
        logging.info('Urls loaded')
    except Exception as e:
        logging.error(e)

    logging.info('Getting products...')

    _products = db.get_products()

    logging.info('{} Products obtained from the database'.format(len(_products)))

    for product in _products:
        logging.info('Fetching price for product ID: {}'.format(product.id))

        current_product = None

        current_product = getattr(shops, re.search(R'[\w\d]*\.([\w\d]+)\.\w{2,3}/', product.url).group(1).capitalize())(product.id, product.url)

        if current_product.price == -1.0:
            continue

        if current_product is not None and db.is_cheapest( current_product.id, current_product.price ):
            logging.info('The product with ID: {} is cheaper'.format(product.id))
            notifications.Telegram.cheapest_product( _config['tg_token'], _config['tg_chat_id'], product.url, product.name, current_product.price, db.get_prices( product.id ).last().price)

        if current_product is not None:
            db.insert_price(current_product.id, current_product.price)
        
            
    logging.info('All Done!')


if __name__ == '__main__':
    config = set_up()
    run(config)
