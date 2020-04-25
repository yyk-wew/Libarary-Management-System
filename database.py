# !_*_ coding:utf-8 _*_

import pymysql
import configparser


class SQLConn(object):
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read("dbinfo.conf")
        db_host = cf.get("db", "db_host")
        db_port = cf.getint("db", "db_port")
        db_user = cf.get("db", "db_user")
        db_pass = cf.get("db", "db_pass")
        db_name = cf.get("db", "db_name")
        self.conn = pymysql.connect(host=db_host, port=db_port, user=db_user, passwd=db_pass, db=db_name)
        self.cursor = self.conn.cursor()

    def cur(self):
        return self.cursor

    def execute(self, instruction):
        self.cursor.execute(instruction)

    def commit(self):
        self.cursor.connection.commit()

    def fetch_result(self, keylist):
        r = self.cursor.fetchall()
        mlist = []
        l = len(keylist)
        if r:
            for tup in r:
                res = {}
                for i in range(l):
                    res[keylist[i]] = str(tup[i])
                mlist.append(res)
        return mlist

    def fetch_result_list(self):
        r = self.cursor.fetchall()
        mlist = []
        if r:
            for tup in r:
                mlist.append(tup[0])
        return mlist

    def close(self):
        self.cursor.close()
        self.conn.close()


def select_sql(table, keys, conditions=''):
    """
    查询语句
    :param table:表名
    :param keys: 需要查询的属性
    :param conditions: 查询条件
    :return: 可执行查询语句
    """
    sql = 'select  %s ' % ",".join(keys)
    sql += ' from %s ' % table
    if conditions:
        sql += ' where %s ' % conditions
    return sql


def delete_sql(table, conditions):
    """
    删除语句
    :param table: 表名
    :param conditions: 删除条件
    :return: 可执行删除语句
    """
    sql = 'delete from  %s  ' % table
    if conditions:
        sql += ' where %s ' % conditions
    return sql


def update_sql(table, updating, conditions=''):
    """
    更新语句
    :param table: 表名
    :param updating: 需要更新的属性
    :param conditions: 属性筛选条件
    :return: 可执行更新语句
    """
    sql = 'update %s set ' % table
    sql += updating
    if conditions:
        sql += ' where %s ' % conditions
    return sql


def insert_sql(table, attrList, valueList):
    """
    插入语句
    :param table: 表名
    :param attrList: 属性列表
    :param valueList: 值列表
    :return: 可执行插入语句
    """
    sql = 'insert into %s (' % table
    sql += ','.join(attrList)
    sql += ') value('
    sql += ','.join(valueList)
    sql += ')'
    return sql


"""
database = SQLConn()
select = select_sql('Users', ['UserID', 'Password'])
print(select)
database.execute(select)
res = database.fetch_result(['UserID', 'Password'])
print(res)
"""
