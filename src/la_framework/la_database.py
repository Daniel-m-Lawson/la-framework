# la_framework/la_database.py
from __future__ import annotations
from contextlib import contextmanager
from typing import Generator, Sequence, TypeVar, Optional
import pyodbc

T = TypeVar("T")


class LaDatabase:
    """Base framework class for interacting with a SQL Server database safely."""

    def __init__(
        self,
        server: str,
        database: str,
        trusted_connection: bool = True,
        user: str | None = None,
        password: str | None = None,
        driver: str = "ODBC Driver 18 for SQL Server",
    ):
        self.server = server
        self.database = database
        self.driver = driver
        self.trusted_connection = trusted_connection
        self.user = user
        self.password = password
        self._conn: pyodbc.Connection | None = None

    def _connect(self) -> pyodbc.Connection:
        """Return an active connection, creating it if necessary."""
        if self._conn is None:
            if self.trusted_connection:
                conn_str = (
                    f"DRIVER={{{self.driver}}};"
                    f"SERVER={self.server};DATABASE={self.database};"
                    "Trusted_Connection=yes;"
                )
            else:
                conn_str = (
                    f"DRIVER={{{self.driver}}};"
                    f"SERVER={self.server};DATABASE={self.database};"
                    f"UID={self.user};PWD={self.password};"
                )
            self._conn = pyodbc.connect(conn_str)
        return self._conn

    @contextmanager
    def cursor(self) -> Generator[pyodbc.Cursor, None, None]:
        """Context manager to safely get a cursor and commit/rollback transactions."""
        conn = self._connect()
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    def execute(self, query: str, params: tuple | None = None) -> None:
        """Execute a query without returning results."""
        with self.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)

    def fetchall(self, query: str, params: tuple | None = None) -> Sequence[pyodbc.Row]:
        """Execute a query and return all rows."""
        with self.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return cur.fetchall()

    def fetchone(self, query: str, params: tuple | None = None) -> Optional[pyodbc.Row]:
        """Execute a query and return a single row."""
        with self.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return cur.fetchone()
