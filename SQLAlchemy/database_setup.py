# import sys
#
# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
# from sqlalchemy import create_engine
#
# # Let's sqlalchemy know that our classes are tables in our db
# Base = declarative_base()
#
#
#
# class Restaurant(Base):
#     __tablename__ = 'restaurant'
#     name = Column(String(80), nullable=False)
#     id = Column(Integer, primary_key=True)
#
#     # def __init__(self, name):
#     #     self.name = name
#
#
# class MenuItem(Base):
#     __tablename__ = 'menu_item'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(80), nullable=False)
#     course = Column(String(255))
#     description = Column(String(250))
#
#     price = Column(String(8))
#     restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
#
#     restaurant = relationship(Restaurant)
#
# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.create_all(engine)
#
# ### CREATE STUFF
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
#
# session = DBSession()
#
# newEntry = Restaurant(name="Kairi's Pizza")
# session.add(newEntry)
# session.commit()
#
# session.query(Restaurant).all()
#
# cheesePizza = MenuItem(name="Kairi's Cheese Pizza", course="Entree", description="Pizza with cheese", price="9.99", restaurant=newEntry)
# session.add(cheesePizza)
# session.commit()
#
# print(session.query(MenuItem).all())

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


engine = create_engine('sqlite:///restaurantmenuwithusers.db')


Base.metadata.create_all(engine)