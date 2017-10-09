import os,sys
from sqlalchemy import Column, ForeignKey, INTEGER, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__='restaurant'
    id = Column(INTEGER,primary_key=True)
    name  = Column(String(250),nullable=False)
class MenuItem(Base):
    __tablename__= 'menu_item'
    name = Column(String(80),nullable=False)
    id = Column(INTEGER,primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(INTEGER,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name':self.name,
            'description':self.description,
            'id':self.id,
            'price':self.price,
            'course':self.course,
        }

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)