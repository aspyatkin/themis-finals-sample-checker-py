# -*- coding: utf-8 -*-
from time import sleep
from random import randrange, choice
from themis.finals.checker.result import Result
from string import ascii_letters, digits
import logging

logger = logging.getLogger(__name__)


def get_random_message():
    return ''.join(choice(ascii_letters + digits) for _ in range(16))


def push(endpoint, capsule, label, metadata):
    delay = randrange(1, 5)
    logger.debug('Sleeping for {0} seconds...'.format(delay))
    sleep(delay)
    return Result.UP, label, get_random_message()


def pull(endpoint, capsule, label, metadata):
    delay = randrange(1, 5)
    logger.debug('Sleeping for {0} seconds...'.format(delay))
    sleep(delay)
    return Result.UP, get_random_message()
