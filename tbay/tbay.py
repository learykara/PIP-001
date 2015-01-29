
from datetime import datetime

from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, Float,
    ForeignKey, Table)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://karaleary:karaleary@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

bid_table = Table(
    'tbay_bids', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('user_id', Integer, ForeignKey('users.id')))

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship("User", secondary="tbay_bids", backref="items_bid_on")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    items_for_sale = relationship("Item", uselist=True, backref="owner_id")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)


Base.metadata.create_all(engine)

