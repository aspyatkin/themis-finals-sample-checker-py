# -*- coding: utf-8 -*-
from themis.checker import Server, Result
from time import sleep
from random import randrange


class SampleChecker(Server):
    def push(self, endpoint, flag, adjunct, metadata):
        sleep(randrange(1, 5))
        return Result.UP, adjunct

    def pull(self, endpoint, flag, adjunct, metadata):
        sleep(randrange(1, 5))
        return Result.UP


checker = SampleChecker()
checker.run()
