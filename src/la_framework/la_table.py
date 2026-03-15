class LaTable(Generic[T]):
    """Framework helper for storing a dataclass in a database table."""

    def __init__(self, db: LaDatabase, table_name: str, dataclass_type: Type[T]):
        self.db = db
        self.table_name = table_name
        self.dataclass_type = dataclass_type

    def insert(self, item: T) -> None:
        """Insert a dataclass instance into the table."""
        data = asdict(item)
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        values = tuple(data.values())
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        self.db.execute(query, values)

    def insert_many(self, items: list[T]) -> None:
        """Insert multiple dataclass instances efficiently."""
        if not items:
            return
        data = [tuple(asdict(item).values()) for item in items]
        columns = ", ".join(asdict(items[0]).keys())
        placeholders = ", ".join("?" for _ in asdict(items[0]))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        with self.db.cursor() as cur:
            cur.fast_executemany = True
            cur.executemany(query, data)

    def fetch_all(self) -> list[T]:
        """Fetch all rows and convert to dataclass instances."""
        query = f"SELECT * FROM {self.table_name}"
        rows = self.db.fetchall(query)
        result = []
        for row in rows:
            # Convert tuple to dataclass using field order
            result.append(self.dataclass_type(*row))
        return result
