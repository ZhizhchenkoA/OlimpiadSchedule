import aiosqlite
import asyncio
import logging


async def create_db(database):
    async with aiosqlite.connect(database) as db:
        return db


class Table:
    def __init__(self, db):
        self.db = db




