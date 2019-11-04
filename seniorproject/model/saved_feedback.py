"""Model to represent saved feedback"""
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'Devon Welcheck'

BASE = declarative_base()


class SavedFeedback(BASE):
    """Model to represent saved feedback"""
    __tablename__ = 'tableNameHere'  # TODO: Put table name here.

    id = Column(Integer, primary_key=True)
    # TODO: Rest of attributes here
