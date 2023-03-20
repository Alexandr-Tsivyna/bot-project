from database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, ForeignKey, Table, MetaData, ForeignKeyConstraint, Text
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy.orm import relationship, relation


class Client(Base):
    __tablename__ = 'users'
    id = Column(GUID, primary_key=True, unique=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    telegram_id = Column(String, unique=True)
    client_info = relationship("ClientsDetails")


class Diet(Base):
    __tablename__ = 'diets'
    id = Column(GUID, primary_key=True, unique=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    description = Column(Text, nullable=False)


class ClientsDetails(Base):
    __tablename__ = 'clients_details'
    id = Column(GUID, primary_key=True, unique=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    user_id = Column(String, ForeignKey('users.telegram_id'), nullable=False)
    diet = Column(GUID, ForeignKey('diets.id'), nullable=False)


class DietDetails(Base):
    __tablename__ = 'diet_details'
    id = Column(GUID, primary_key=True, unique=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    diet = Column(GUID, ForeignKey('diets.id'))
    product = Column(GUID, ForeignKey('products.id'))


class Food(Base):
    __tablename__ = 'products'
    id = Column(GUID, unique=True, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
    name = Column(String)
    kal = Column(String, nullable=False)
    product_info = relationship("DietDetails")

