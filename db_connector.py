from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import os
from flask_user import UserMixin
engine = create_engine("mysql://{}:{}@localhost/dnd".format("dnd", "add8487ec4"))

Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)

class DNDModel:

    @classmethod
    def get_all(cls):
        session = Session()
        try:
            return session.query(cls).all()
        except Exception as e:
            return []
        finally:
            session.expunge_all()
            session.close()
    @classmethod
    def get_by_id(cls, i):
        session = Session()
        try:
            return session.query(cls).get(i)
        except Exception as e:
            return None
        finally:
            session.expunge_all()
            session.close()

    def commit(self):
        session = Session()
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            raise e
        finally:
            session.expunge(self)
            session.close()

class User(Base, DNDModel, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(username={})>".format(self.username)

class Stat(Base, DNDModel):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer)
    stat_id = Column(Integer)
    value = Column(Integer)

    def __repr__(self):
        return "<Stat(character_id={}, stat_id={}, value={})>".format(self.character_id, self.stat_id, self.value)

    @classmethod
    def get_by_character(cls, cid):
        session = Session()
        try:
            return session.query(cls).filter_by(character_id=cid).all()
        except Exception as e:
            return []
        finally:
            session.expunge_all()
            session.close()

class Achievement(Base, DNDModel):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<Achievement(name={}, desc={})>".format(self.name, self.description)


class StatType(Base, DNDModel):
    __tablename__ = "stat_types"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "StatType<name={}>".format(self.name)

class Character(Base, DNDModel):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "Character<name={}>".format(self.name)

def get_user_by_id(i):
    session = Session()
    try:
        return session.query(User).get(i)
    except Exception as e:
        return None

def get_user_by_username(username):
    session = Session()
    try:
        return session.query(User).filter_by(username=username)[0]
    except Exception as e:
        raise e

def check_password(username, password):
    pass


