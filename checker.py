# -*- coding: utf-8 -*-
from time import sleep
from random import randrange
from themis.finals.checker.result import Result


def push(endpoint, flag, adjunct, metadata):
    sleep(randrange(1, 5))
    return Result.UP


def pull(endpoint, flag, adjunct, metadata):
    sleep(randrange(1, 5))
    return Result.UP
