from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Users(Base):
    __tablename__ = 'userdata'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    image = Column(String(120), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'email': self.description,
           'id': self.id,
           'image': self.price,
               }


class Brands(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('userdata.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'user_id': self.user_id
                }


class Items(Base):
    __tablename__ = 'brand_item'

    name = Column(String(80), nullable=False)
    image = Column(String(120), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    price = Column(String(8))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship(Brands)
    user_id = Column(Integer, ForeignKey('userdata.id'))
    user = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'description': self.description,
           'id': self.id,
           'price': self.price,
           'user_id': self.user_id
               }


engine = create_engine('sqlite:///brandProducts.db')


Base.metadata.create_all(engine)
