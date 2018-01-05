import sched, time
import requests
import json
import datetime
import product


s = sched.scheduler(time.time, time.sleep)
apiBase = 'https://api.quoine.com/'

def check_price(productId, lowerLimit):
    r = requests.get(apiBase + '/products/' + productId)
    data = json.loads(r.text)
    info = {}
    info['text'] = '{0} - {1} buy: {2}, sell: {3}'.format(datetime.datetime.now().strftime("%I:%M%p"), data['currency_pair_code'], data['market_bid'], data['market_ask'])
    print(info)
    
    if data['market_bid'] >= lowerLimit:
        requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

def qash_margin_calculator():
    print('i am test')
    
    targetData = get_all()
    
    start = 100
    qashusd = 0
    qasheth = 0
    ethusd = 0
    qashbtc = 0
    btcusd = 0
    ethbtc = 0
    print(product.Product.qashusd.value)
    for data in targetData:
      if(int(data['id'])==product.Product.qashusd.value):
        qashusd = float(data['low_market_bid'])

      if(int(data['id'])==product.Product.qasheth.value):
        qasheth = float(data['low_market_bid'])

      if(int(data['id'])==product.Product.ethusd.value):
        ethusd = float(data['low_market_bid'])

      if(int(data['id'])==product.Product.qashbtc.value):
        qashbtc = float(data['low_market_bid'])

      if(int(data['id'])==product.Product.btcusd.value):
        btcusd = float(data['low_market_bid'])

      if(int(data['id'])==product.Product.ethbtc.value):
        ethbtc = float(data['low_market_bid'])
    

    raw = start * qashusd
    

    ethflow = start * qasheth * ethusd
    btcflow = start * qashbtc * btcusd
    ethbtcflow = start * qasheth * ethbtc * btcusd
    info = {}
    info['text'] = 'qashusd: {0}'.format(qashusd)

    requests.post("https://hooks.slack.com/services/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", data={"payload": "i am starting..."})
    requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    if ethflow/raw >= 1.1:
      info['text'] = 'ethflow margin: {0} qasheth: {1} ethusd: {2}'.format(ethflow/raw,qasheth,ethusd)
      requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    if btcflow/raw >= 1.1:
      info['text'] = 'btcflow margin: {0} qashbtc: {1} btcusd: {2}'.format(btcflow/raw,qashbtc,btcusd)
      requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    if ethbtcflow/raw >= 1.1:
      info['text'] = 'ethbtcflow margin: {0} qasheth: {1} ethbtc: {2} btcusd: {3}'.format(ethbtcflow/raw,qasheth,ethbtc,btcusd)
      requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})


def get_all():
    r = requests.get(apiBase + '/products/')
    data = json.loads(r.text)
    targetData = [x for x in data if int(x['id']) in list(map(int,product.Product))]
    return targetData

def scheduler(s):
   s.enter(3000, 1, qash_margin_calculator)
   s.enter(3000, 1, check_price, argument=('57', 1))
   s.enter(3000, 1, check_price, argument=('59', 1.3))
   s.run()

qash_margin_calculator()

while(1):
    scheduler(s)