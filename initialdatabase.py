import mysqlop
table = {
    'BUFF': {
        'goods_name_buff': 'CHAR(50)',
        'info_price_buff': 'DECIMAL(11,4)'
    },
    'IGXE': {
        'goods_name_igxe': 'CHAR(50)',
        'info_price_igxe': 'DECIMAL(11,4)'
    },
    '`MAX`': {
        'goods_name_max': 'CHAR(50)',
        'info_price_max': 'DECIMAL(11,4)'
    },
    "`comp`": {
        'name_of_max_price': 'CHAR(50)',
        'max_price': 'DECIMAL(11,4)',
        'name_of_min_price': 'CHAR(50)',
        'min_price': 'DECIMAL(11,4)',
        'diff': 'CHAR(30)'
    },
    'cheap': {
        'cheap_price': 'DECIMAL(11,4)',
        'cheap_name': 'CHAR(50)'
    }
}


def initial_all():
    mysqlop.initial_db(table)


# 删除所有表
def delete_all():
    for name, i in table.items():
        # 获取数据库光标
        db, cur = mysqlop.connect2db()
        # 调用函数删除指定名称的表
        mysqlop.delete_table(cur, name)
        # 关闭数据库
        mysqlop.disconnect4db(cur, db)


def add_all_value(name, values):
    database, cursor = mysqlop.connect2db()
    for value in values:
        mysqlop.add_value(cursor, name, value)
    database.commit()
    mysqlop.disconnect4db(cursor, database)
