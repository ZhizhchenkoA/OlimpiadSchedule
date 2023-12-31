from __future__ import annotations
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship, Session)
from sqlalchemy import Column, create_engine, ForeignKey, Table, Engine
from typing import Optional, List, Set, NoReturn
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users_telegram.id"), primary_key=True),
    Column("olimpiad_id", ForeignKey("olimpiads.id"), primary_key=True),
)


class UserTelegram(Base):
    __tablename__ = 'users_telegram'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    settings: Mapped[Optional["Settings"]] = relationship(back_populates="user")
    subscriptions: Mapped[Optional[Set["Olimpiad"]]] = relationship(secondary=association_table, back_populates="users")

    def __repr__(self):
        return f'{self.telegram_id} - {[i for i in self.subscriptions]}'


class Settings(Base):
    __tablename__ = 'settings_table'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user: Mapped[List["UserTelegram"]] = relationship(back_populates="settings")
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users_telegram.id"))
    time_zone: Mapped[Optional[int]] = mapped_column()
    suitable_time: Mapped[Optional[datetime.time]] = mapped_column()
    previous_date: Mapped[Optional[int]] = mapped_column()
    amount: Mapped[Optional[int]] = mapped_column()


class Stage(Base):
    __tablename__ = 'stages'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(default=None)
    beginning_date: Mapped[Optional[datetime.date]] = mapped_column()
    ending_date: Mapped[Optional[datetime.date]] = mapped_column()
    olimpiad: Mapped["Olimpiad"] = relationship(back_populates="stages")
    olimpiad_id: Mapped[int] = mapped_column(ForeignKey('olimpiads.id'))

    def __str__(self):
        return f'{self.name} - {self.description} ({self.beginning_date} - {self.ending_date})'


class Olimpiad(Base):
    __tablename__ = "olimpiads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    private: Mapped[bool] = mapped_column(default=False)
    stages: Mapped[List["Stage"]] = relationship(back_populates="olimpiad")
    users: Mapped[Optional[Set["UserTelegram"]]] = relationship(secondary=association_table,
                                                                back_populates="subscriptions")
    user_in_site: Mapped[Optional[Set["UserSite"]]] = relationship(back_populates="added_olimpiads")

    def __str__(self):
        return f'{self.name} - {self.description} {self.stages}'


class UserSite(Base):
    __tablename__ = "users_site"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_approved: Mapped[bool] = mapped_column(default=False)
    added_olimpiads: Mapped[Optional[Set["Olimpiad"]]] = relationship(back_populates="user_in_site")
    olimpiads_id: Mapped[Optional[int]] = mapped_column(ForeignKey('olimpiads.id'))


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Interaction(metaclass=Singleton):

    def __init__(self, database: str) -> None:
        self.engine: Engine = create_engine(database)
        Base.metadata.create_all(bind=self.engine)
        self.db: Session = Session(bind=self.engine)

    def select_all(self, class_: object) -> List[object]:
        users = self.db.query(class_).all()
        return users

    @staticmethod
    def add_stage(name: str, description: str = None, beginning_date: datetime.date = None,
                  ending_date: datetime.date = None) -> Stage:
        return Stage(name=name, description=description, beginning_date=beginning_date, ending_date=ending_date)

    def add_olimpiad(self, name: str, description: str, stages: List[Stage], private=False) -> Olimpiad:
        olimpiad = Olimpiad(name=name, description=description, private=private)
        olimpiad.stages = stages
        self.db.add(olimpiad)
        self.db.commit()
        return olimpiad

    def find_olimpiad(self, name: str) -> Olimpiad:
        olimpiad = self.db.query(Olimpiad).filter(Olimpiad.name == name).all()
        if olimpiad:
            return olimpiad[0]
        else:
            return None

    def find_olimpiad_by_id(self, id: int) -> Olimpiad:
        olimpiad = self.db.query(Olimpiad).filter(Olimpiad.id == id).all()
        if olimpiad:
            return olimpiad[0]
        else:
            return None

    def find_user_telegram(self, telegram_id: int) -> UserTelegram:
        if user := self.db.query(UserTelegram).filter(UserTelegram.telegram_id == telegram_id).all():
            return user[0]
        return None

    def create_user_telegram(self, telegram_id: int) -> UserTelegram:
        user = UserTelegram(telegram_id=telegram_id)
        self.db.add(user)
        self.db.commit()
        return user

    def add_settings(self, user: UserTelegram, time_zone: int, suitable_time: datetime.time, amount: int,
                     previous_date: int) -> Settings:
        settings = Settings(time_zone=time_zone, suitable_time=suitable_time, amount=amount,
                            previous_date=previous_date)
        user.settings = settings

        self.db.commit()
        return settings

    def del_settings(self, settings):
        self.db.delete(settings)
        self.db.commit()

    def add_subscription(self, user: UserTelegram, olimpiad: Olimpiad) -> UserTelegram:
        if user.subscriptions:
            user.subscriptions.update({olimpiad})
        else:
            user.subscriptions = {olimpiad}
        self.db.commit()
        return user

    def remove_subscription(self, user: UserTelegram, olimpiad: Olimpiad) -> Olimpiad:
        if olimpiad in user.subscriptions:
            user.subscriptions.remove(olimpiad)
            self.db.commit()
        else:
            return None
    def create_site_user(self, user: str, password: str) -> UserSite:
        user_obj = UserSite(user=user, password=password)
        self.db.add(user_obj)
        self.db.commit()
        return user_obj

    def find_user(self, name: str) -> UserSite:
        if user := self.db.query(UserSite).filter(UserSite.name == name).all():
            return user[0]
        else:
            return None

    def site_user_olimpiads(self, user: UserSite, olimpiad: Olimpiad) -> UserSite:
        if user.added_olimpiads:
            user.added_olimpiads.update(olimpiad)
            self.db.commit()
            return user
        else:
            user.added_olimpiads = set(olimpiad)
            self.db.commit()
            return user
