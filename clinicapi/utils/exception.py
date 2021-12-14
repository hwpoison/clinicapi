from dataclasses import dataclass
from fastapi import status


@dataclass
class Exceptional(Exception):
    """
        Exception 
    """
    message: str
    status_code: int


@dataclass
class ResponseInfo():
    """
        Response message
    """
    message: str
