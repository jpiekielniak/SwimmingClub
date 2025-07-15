import sqlite3
from webapp.queries import (
    SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION,
    SQL_SESSIONS,
    SQL_SWIMMERS_BY_SESSION,
    SQL_SWIMMERS_EVENTS_BY_SESSION,
)

DB_PATH = "webapp/TrainingsDB.sqlite3"


def get_sessions():
    """Return a list of unique training session timestamps."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(SQL_SESSIONS)
        return cursor.fetchall()


def get_swimmers_by_session(date: str):
    """Return a list of (name, age) tuples for swimmers in a given session date."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(SQL_SWIMMERS_BY_SESSION, (date,))
        return cursor.fetchall()


def get_events_for_swimmer(name: str, age: int, date: str):
    """Return a list of events for a swimmer on a given date."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(SQL_SWIMMERS_EVENTS_BY_SESSION, (name, age, date))
        return cursor.fetchall()


def get_times_for_swimmer(name: str, age: int, distance: str, stroke: str, date: str):
    """Return a list of times for a swimmer for a given event and date."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            SQL_CHART_DATA_BY_SWIMMER_EVENT_SESSION,
            (name, age, distance, stroke, date),
        )
        return cursor.fetchall()
