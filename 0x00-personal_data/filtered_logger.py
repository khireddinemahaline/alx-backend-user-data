#!/usr/bin/env python3
""" Filtered logger """


import re
import logging
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields: List[str], redaction:str, message:List[str], separator:str) -> str:
    """Filter data"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}', f'{field}={redaction}{separator}', message)
    return message

    


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Format log record"""
        return filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)

def get_logger() -> logging.Logger:
    """Get logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
    return logger