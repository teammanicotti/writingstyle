"""Example of SQLAlchemy interaction"""
from seniorproject.db.db_connector import DBConnector

__author__ = 'Devon Welcheck'


class RecommendationUtilityExample:
    """Example of SQLAlchemy interaction."""
    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def do_stuff(self):
        """Doing stuff here."""
        with self.db_connector.start_session(auto_commit=True):
            # Do stuff here.  if you do not auto-commit,
            # commit it before exiting the scope of the `with` statement.
            pass
