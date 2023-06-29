from typing import Dict, Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedularMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str | Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]):
        data['appschedulet'] = self.scheduler
        return await handler(event, data)
