from flask_rq2 import RQ
from rq import get_current_job
import requests
import random
import simplejson
import json
import time

# (production)
import redis
r = redis.Redis(host='redis', port=6379, db=0)

rq = RQ()
rq.redis_url = 'redis://redis:6379/0'

# from rq_scheduler import Scheduler
# from datetime import datetime
# scheduler = Scheduler(connection=Redis())

# scheduler.schedule(
#     scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
#     func=callSpotify,                     # Function to be queued
#     interval=60,                   # Time before the function is called again, in seconds
#     repeat=None,                     # Repeat this number of times (None means repeat forever
# )


# (development only) insert easydbio creds and instantiate object...

# db = easydbio.DB({
#   "database": "5741e0d0-68ab-447e-8488-24ca97755690",
#   "token": "70e331da-07d9-4259-917a-246232b3a26d"
# })

@rq.job(timeout=180)
def analyzeDocs():
    self_job = get_current_job()

    from buzzScore import buzzScore

    b = buzzScore()
    data = b.compute()
    data = data.to_dict()
    r.set('data',str(data))

    self_job.meta['progress'] = {'num_iterations': 1, 'iteration': 1, 'percent': 100}
    # save meta information to queue
    self_job.save_meta()
    time.sleep(2)
    return curr