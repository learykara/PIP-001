
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
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship('Bid', uselist=True, backref='bids_on_item')

    def max_bid(self):
        """Return the price of the highest bid on the item
        If no bids have been placed, return 0
        """
        bids = session.query(Bid).filter_by(item_id = self.id)
        return [0 if len(bids) == 0 else max([bid.price for bid in bids])]

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    items_for_sale = relationship('Item', uselist=True, backref='owner')
    bids = relationship('Bid', uselist=True, backref='bid_owner')

    def bid_on_item(self, item_id, price):
        """Add an entry to the `bids` table representing a bid on the
        Item with id = `item_id`

        If the item doesn't exist, raise an error

        Return the id of the bid
        """
        item = session.query(Item).get(item_id)
        if item is None:
            # return error? none?
            pass
        if price <= item.max_bid():
            # return error?
            pass
        bid_made = Bid(price=price, item_id=item_id, user_id=self.id)
        return bid_made.id


class Bid(Base):
    __tablename__ = 'bids'

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)

    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


Base.metadata.create_all(engine)

