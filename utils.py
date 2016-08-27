# -*- coding: utf-8 -*-
import logging
import os
from sys import stdout
import base64
import hashlib


def get_logger():
    console_handler = logging.StreamHandler(stdout)
    log_format = u'[%(asctime)s] - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    logger = logging.Logger(__name__)
    level_str = os.getenv('LOG_LEVEL', 'INFO')
    if level_str == 'CRITICAL':
        level = logging.CRITICAL
    elif level_str == 'ERROR':
        level = logging.ERROR
    elif level_str == 'WARNING':
        level = logging.WARNING
    elif level_str == 'INFO':
        level = logging.INFO
    elif level_str == 'DEBUG':
        level = logging.DEBUG
    elif level_str == 'NOTSET':
        level = logging.NOTSET
    else:
        level = logging.INFO
    logger.setLevel(level)
    logger.addHandler(console_handler)
    return logger


def issue_token(name):
    nonce_size = int(os.getenv('THEMIS_FINALS_NONCE_SIZE', '16'))

    nonce = os.urandom(nonce_size)
    secret_key = base64.urlsafe_b64decode(
        os.getenv('THEMIS_FINALS_{0}_KEY'.format(name))
    )

    h = hashlib.sha256()
    h.update(nonce)
    h.update(secret_key)

    nonce_bytes = nonce
    digest_bytes = h.digest()

    token_bytes = nonce_bytes + digest_bytes
    return base64.urlsafe_b64encode(token_bytes)


def issue_checker_token():
    return issue_token('CHECKER')


def verify_token(name, token):
    if token is None:
        return False

    nonce_size = int(os.getenv('THEMIS_FINALS_NONCE_SIZE', '16'))

    token_bytes = base64.urlsafe_b64decode(token.encode('utf-8'))

    if len(token_bytes) != 32 + nonce_size:
        return False

    nonce = token_bytes[0:nonce_size]
    received_digest_bytes = token_bytes[nonce_size:]

    secret_key = base64.urlsafe_b64decode(
        os.getenv('THEMIS_FINALS_{0}_KEY'.format(name))
    )

    h = hashlib.sha256()
    h.update(nonce)
    h.update(secret_key)

    digest_bytes = h.digest()

    return digest_bytes == received_digest_bytes


def verify_master_token(token):
    return verify_token('MASTER', token)
