from pymongo import MongoClient
from pymongo.database import Database


class DatabaseConnection:
    client: MongoClient
    db: Database

    def connect(self, uri: str, db_name: str) -> None:
        self.client = MongoClient(uri)
        self.db = self.client[db_name]


database = DatabaseConnection()
