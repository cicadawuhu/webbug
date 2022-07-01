import pymysql
from info_local import uhost, uuser, upasswd, udb



def connect2db(host=uhost, user=uuser, passwd=upasswd, db=udb):
    db = pymysql.connect(host='%s' % host, user="%s" % user, password="%s" % passwd, database="%s" % db)
    cursor = db.cursor()
    return db, cursor


def disconnect4db(cursor, db):
    cursor.close()
    db.close()


def add_field(cursor, tablename, field, charset):
    cursor.execute('ALTER TABLE %s ADD %s %s' % (tablename, field, charset))


def initial_db(names):
    database, cursor = connect2db()
    for name, fields in names.items():
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS %s(`id` int(9) PRIMARY KEY  NOT NULL AUTO_INCREMENT) DEFAULT CHARSET utf8;' % name)
        for field, charset in fields.items():
            add_field(cursor, name, field, charset)
    disconnect4db(cursor=cursor, db=database)


def delete_table(cursor, name):
    cursor.execute('DROP TABLE IF EXISTS %s' % name)


def add_value(cursor, name, values):
    key = values.keys()
    value = values.values()
    col = ','.join(map(str,key))
    place = ','.join(map(str,value))
    cursor.execute('INSERT INTO %s (%s) VALUES(%s);' % (name, col, place))

