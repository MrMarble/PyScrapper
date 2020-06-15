import requests, json

class Telegram():
   
    def cheapest_product(_bot_token, _chat_id, _url, _product_name, _actual_price, _previous_price):
        url = 'https://api.telegram.org/bot{}/sendmessage'.format(_bot_token)
        payload = {
            'chat_id': _chat_id,
            'text': '[⚠️]({}) El producto `{}` esta mas barato. *{}€*, antes {}€.'.format(_url,_product_name,_actual_price,_previous_price),
            'parse_mode': 'markdown'
        }
        headers = {'content-type': 'application/json'}
        requests.post(url, data=json.dumps(payload), headers=headers)