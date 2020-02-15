from buzzScore import buzzScore

b = buzzScore()
data = b.compute()

import redis
r = redis.Redis(host='192.168.99.100', port=6379, db=0)
data = data.to_dict()

r.set('data',str(data))

data_got=eval(r.get('data'))
print(data_got['Java'])