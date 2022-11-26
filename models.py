from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, \
     ForeignKey, event, Float, select
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data.db', convert_unicode=True)
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    Model.metadata.create_all(bind=engine)


Model = declarative_base(name='Model')
Model.query = session.query_property()


class CRUD():

    def save(self):
        if self.id == None:
            session.add(self)
        return session.commit()

    def destroy(self):
        session.delete(self)
        return session.commit()


class Spreadsheet(Model, CRUD):
    __tablename__ = 'spreadsheets'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(200))
    date = Column('date', Date)
    amount = Column('amount', Float)

    def __init__(self, name, date, amount):
        self.name = name
        self.date = date
        self.amount = amount

    def credits(self):
        # return self.amount >= 0
        # return session.query(self).filter(self.amount >= 0)
        stmt = select(self).where(self.amount >= 0)
        return session.execute(stmt)

    def debits(self):
        return session.query(self).filter(self.amount < 0)

    def __repr__(self):
        return "Spreadsheet()"

    def __str__(self):
        return "member of spreadsheet"

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)