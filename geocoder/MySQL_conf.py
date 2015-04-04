import logging
import os
import sys
import MySQLdb

def import_conf(mode):
    names = __name__.split('.')
    names[-1] = '{0}_conf'.format(mode.lower())
    name = '.'.join(names)
    if name not in sys.modules:
        __import__(name)
    return sys.modules[name]

def orm_config(mode):
    try:
        conf = import_conf(mode)
    except ImportError:
        raise RuntimeError('conf file not found: {0}'.format(mode))

    #mysql://punkphysicist:portalshibuya@wikipediaja.c9xyho0gmaha.ap-northeast-1.rds.amazonaws.com/wikipedia?charset=utf8"
    return 'mysql://{user}:{passwd}@{host}/{db}?charset={charset}'.format(
        user=conf.rw_user, passwd=conf.rw_pass,
        host=conf.host, db=conf.db, charset='utf8')
