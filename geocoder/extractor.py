# -*- coding: utf-8; -*-

## The python standard library
import sys
reload(sys)
import codecs
import math
import csv
import re
import time
import os
import os.path
import json
import urllib2
import MeCab

## External Library
# import mojimoji
import geohash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func,create_engine,func,and_
sys.path.append(os.pardir)
from MySQL_conf import orm_config
from models import ContentsSource,Contents,Grasses,GrassLocation


## For contents database to access
Base = declarative_base()
engine=create_engine(orm_config('dev'),echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


## global variable
pttr_ken = re.compile(u'^(京都府|.+?[都道府県])')
delimiters = '; |, |\n|\.|。'
MAX_CHARACTER_RANGE = 150000
LOCK_NUM = 1
LOCATION_LOCK_NUM = 2
### For deal with Japanese text
sys.stdin=codecs.getreader('utf_8')(sys.stdin)
sys.stdout=codecs.getwriter('utf_8')(sys.stdout)
sys.setdefaultencoding('utf-8')

class Point:
    ''''
    Point(latitude,logitude)
    '''
    def __init__(self, latitude,longitude):
        self._latitude = latitude
        self._longitude = longitude
    def __repr__(self):
        return '<Point(%s,%s)>' % (self._latitude,self._longitude)
    @property
    def latitude(self):
        return self._latitude
    @latitude.getter
    def latitude(self):
        return self._latitude
    @property
    def longitude(self):
        return self._longitude
    @longitude.getter
    def longitude(self):
        return self._longitude

class Location:
    '''
    longitude,latitude -> geohash
    '''
    def __init__(self, point=None,grid_start = 0,grid_end = 0,hash_value=None,area_name = ''):
        self._point = point
        self._grid_start = grid_start
        self._grid_end = grid_end
        self._hash_value = hash_value
        self._area_name = area_name

    def __repr__(self):
        return '<Location (%s,grid(%s,%s),%s,%s)>' % (self._point,self._grid_start,self._grid_end,self._hash_value,self._area_name)

    @property
    def hash_value(self):
        return self._hash_value

    @hash_value.getter
    def hash_value(self):
        if(self._hash_value == None):
            self._hash_value = geohash.encode(self._point.latitude,self._point.longitude)
        return self._hash_value

def wakati_gaki(texts):
    tagger = MeCab.Tagger("-Ochasen")
    ret = []
    node = tagger.parseToNode(texts)
    while node:
        word = []
        line = node.feature
        print line
        if line.split(',')[-3] != "*":
            ret.append(line.split(','))
        node = node.next
    return ret

def article2locations(text):
    '''
    input: text
    output: [{index:102,areatag:chiba},...]
    '''
    wakati = wakati_gaki(text)
    lock=False
    word=''
    word_loc=''
    location_lock = 0
    locs=[]
    for i in wakati:
        word=i[-3]
        type=i
        if word=='@': continue
        #print word, type
        if not (type[1] in [u'数'] or type[2] in [u'地域',u'助数詞'] or word==u'*' or type[3] in [u'国']):
            lock=False
            if word_loc:
                location_lock = LOCATION_LOCK_NUM
                locs.append(word_loc)
                word_loc=''
        else:
            if word :
                ## Unite '地域(area)' word and '助数詞(number)' word.
                if not lock and type[2]==u'地域':
                    word_loc=word
                    lock=True
                elif lock:
                    word_loc+=word.replace(u'・',' ')
        ## location check phase
        if location_lock > 0:
            ## if word lock is going on, then stop to count location lock
            if lock is False:
                location_lock -= 1
            if location_lock == 0:
                # locations = areatags2locations(areatags = locs)
                for loc in locs:
                    print loc
#                 if locations != []:
#                     logger.info( 'extracted locations:' + str(count) + '. ' + article.title)
                    # for location in locations:
                        # add_areatag_contents(article,location['area_tags'])
#                     logger.info( '=>' + ",".join(location['area_tags'].area_tag))
#                     elapsed_time = time.time() - start
#                     logger.info("elapsed_time:{0}".format(elapsed_time))
                ## location should be empty
                # locs = []
    # locations = areatags2locations(areatags = locs)
    return locs




if __name__=="__main__":
    argvs = sys.argv
    argc = len(sys.argv)
    if argc != 3:
        print("usage: $ %s <since> <until>" % (argvs[0]))
        print("example: $ %s '2014-02-25 00:00:00' '2015-02-25 00:00:00'" % (argvs[0]))
        exit()
    since,until = argvs[1],argvs[2]
    init_logger()

