from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import os
engine = create_engine("mysql://{}:{}@localhost/dnd".format(os.environ.get("DB_USER"), os.environ.get("DB_PASS")))

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(username={})>".format(self.username)

class Stat(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer)
    stat_id = Column(Integer)
    value = Column(Integer)

    def __repr__(self):
        return "<Stat(character_id={}, stat_id={}, value={})>".format(self.character_id, self.stat_id, self.value)

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<Achievement(name={}, desc={})>".format(self.name, self.description)


class StatType(Base):
    __tablename__ = "stat_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "StatType<name={}>".format(self.name)

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "Character<name={}>".format(self.name)
