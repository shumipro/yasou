# License:  MIT License
# Created:  2014/10/21
# Project:  bitbucket/kamelio_location
# Comment:
# - Reference list -
# xxx
# ------------------
# -*- coding: utf-8 -*-
#
import sys
import os
# import re
# import unittest
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func,create_engine
# sys.path.append(os.pardir)
from MySQL_conf import orm_config

# For analyze message

# Global variable
# local_PASSWORD = ''
# local_USER_NAME = 'root'

## For contents database to access
Base = declarative_base()
engine=create_engine(orm_config('dev'),echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Content source
class ContentsSource(Base):
    __tablename__ = 'contents_source'
    id=Column(sa.Integer, primary_key=True)
    source_name=Column(sa.String(50))


class Contents(Base):
    __tablename__ = 'contents'
    id=Column(sa.BigInteger, primary_key=True)
    source_id=Column(sa.Integer)
    title=Column(sa.String(200))
    body=Column(sa.Text)
    body_text=Column(sa.Text)
    link=Column(sa.String(1000))
    date_added=Column(sa.DateTime)
    date_body_added=Column(sa.DateTime)
    date_published=Column(sa.DateTime)


class Grasses(Base):
    __tablename__ = 'grasses'
    id = Column(sa.BigInteger,primary_key = True)
    name = Column(sa.String(100))
    name_en = Column(sa.String(100))
    tokyo_area = relationship('Areamaster',
    secondary = 'AREATAG_AREA',
    backref = 'areatag'
    )

class GrassLocation(Base):
    __tablename__ = 'grass_location'
    id = Column(sa.BigInteger,primary_key = True)
    grass_id = Column(sa.BigInteger)
    contents_id = Column(sa.BigInteger)
    img=Column(sa.Text)
    img_cache=Column(sa.String(500))
    image_size=Column(sa.String(1000))
    address = Column(sa.String(100))
    lon = Column(sa.Float)
    lat = Column(sa.Float)

if __name__ == '__main__':
    # Make all database on local
    Base.metadata.create_all(engine)

