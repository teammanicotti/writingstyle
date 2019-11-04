"""Provides interface to database instance"""
from typing import Generator
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

__author__ = 'Devon Welcheck'


class DBConnector:
    """Provides interface to database instance"""
    def __init__(self, connection):
        self.connection = connection
        self.engine = sqlalchemy.create_engine(self.connection)
        self.session_factory = orm.sessionmaker(
            bind=self.engine,
            autocommit=False
        )

    @contextmanager
    def start_session(self, auto_commit) -> Generator[Session, None, None]:
        """Creates an auto-closing session instance from the factory
        Implements http://yxdong.me/posts/sqlalchemy-session-usage-patterns-in-web-applications.html.  # pylint: disable=line-too-long
        :param auto_commit: whether to automatically commit a transaction when
        it goes out of scope
        :return: Generator[Session]
        """
        session = self.session_factory()
        try:
            yield session
            if auto_commit:
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
