# -*- coding: utf-8 -*-
from rq import Connection, Worker
from redis import Redis
import os

import worker

with Connection(Redis(
        host=os.getenv('REDIS_HOST', '127.0.0.1'),
        port=int(os.getenv('REDIS_PORT', '6379')),
        db=int(os.getenv('REDIS_DB', '0')))):
    Worker(['default']).work()
