# -*- coding: utf-8 -*-
from utils import get_logger
from datetime import datetime
import dateutil.parser
from dateutil.tz import tzlocal
import base64
from enum import Enum
from time import sleep
from random import randrange
from sys import exc_info
import requests
from utils import issue_checker_token
import os


logger = get_logger()


class Result(Enum):
    UP = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    INTERNAL_ERROR = 110


def push(endpoint, flag, adjunct, metadata):
    sleep(randrange(1, 5))
    return Result.UP, adjunct


def pull(endpoint, flag, adjunct, metadata):
    sleep(randrange(1, 5))
    return Result.UP


def internal_push(endpoint, flag, adjunct, metadata):
    result, updated_adjunct = Result.INTERNAL_ERROR, adjunct
    try:
        result, updated_adjunct = push(endpoint, flag, adjunct, metadata)
    except Exception:
        logger.exception('An exception occurred', exc_info=exc_info())
    return result, updated_adjunct


def internal_pull(endpoint, flag, adjunct, metadata):
    result = Result.INTERNAL_ERROR
    try:
        result = pull(endpoint, flag, adjunct, metadata)
    except Exception:
        logger.exception('An exception occurred', exc_info=exc_info())
    return result


def queue_push(job_data):
    params = job_data['params']
    metadata = job_data['metadata']
    timestamp_created = dateutil.parser.parse(metadata['timestamp'])
    timestamp_delivered = datetime.now(tzlocal())

    status, updated_adjunct = internal_push(
        params['endpoint'],
        params['flag'],
        base64.b64decode(params['adjunct']),
        metadata)

    timestamp_processed = datetime.now(tzlocal())

    job_result = dict(status=status.value,
                      flag=params['flag'],
                      adjunct=base64.b64encode(updated_adjunct))

    delivery_time = (timestamp_delivered - timestamp_created).total_seconds()
    processing_time = (
        timestamp_processed - timestamp_delivered
    ).total_seconds()

    log_message = (u'PUSH flag `{0}` /{1:d} to `{2}`@`{3}` ({4}) - status {5},'
                   u' adjunct `{6}` [delivery {7:.2f}s, processing '
                   u'{8:.2f}s]').format(
        params['flag'],
        metadata['round'],
        metadata['service_name'],
        metadata['team_name'],
        params['endpoint'],
        status.name,
        job_result['adjunct'],
        delivery_time,
        processing_time
    )

    logger.info(log_message)

    uri = job_data['report_url']
    headers = {}
    headers[os.getenv('THEMIS_FINALS_AUTH_TOKEN_HEADER')] = \
        issue_checker_token()
    r = requests.post(uri, headers=headers, json=job_result)
    logger.info(r.status_code)


def queue_pull(job_data):
    params = job_data['params']
    metadata = job_data['metadata']
    timestamp_created = dateutil.parser.parse(metadata['timestamp'])
    timestamp_delivered = datetime.now(tzlocal())

    status = internal_pull(
        params['endpoint'],
        params['flag'],
        base64.b64decode(params['adjunct']),
        metadata)

    timestamp_processed = datetime.now(tzlocal())

    job_result = dict(request_id=params['request_id'],
                      status=status.value)

    delivery_time = (timestamp_delivered - timestamp_created).total_seconds()
    processing_time = (
        timestamp_processed - timestamp_delivered
    ).total_seconds()

    log_message = (u'PULL flag `{0}` /{1:d} from `{2}`@`{3}` ({4}) with '
                   u'adjunct `{5}` - status {6} [delivery {7:.2f}s, '
                   u'processing {8:.2f}s]').format(
        params['flag'],
        metadata['round'],
        metadata['service_name'],
        metadata['team_name'],
        params['endpoint'],
        params['adjunct'],
        status.name,
        delivery_time,
        processing_time
    )

    logger.info(log_message)

    uri = job_data['report_url']
    headers = {}
    headers[os.getenv('THEMIS_FINALS_AUTH_TOKEN_HEADER')] = \
        issue_checker_token()
    r = requests.post(uri, headers=headers, json=job_result)
    logger.info(r.status_code)
