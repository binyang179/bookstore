# -*- coding:utf-8 -*-
"""
定义一组数据库操作函数
"""

import MySQLdb as sqldb

HOST = "localhost"
# 你自己的数据库登录用户名
USER = "root"
# 你自己的数据库登录密码
PASSWORD = "Passw0rd"
# 你自己的数据库名称
DB = "mall"
CHARSET = "utf8"


def get_connection():
    """
    创建一个数据库连接
    :return:
    """
    db_connect = sqldb.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET)
    return db_connect


def query(sql, call_back, parameters=None):
    """
    执行查询（Select语句）
    :param sql: 要执行的Select语句
    :param call_back: 从查询结果中获取对应的结果，是一个函数
    :param parameters: 与Select语句对应的参数
    :return:
    """
    try:
        connect = get_connection()   # 创建数据库连接
        cursor = connect.cursor()    # 创建游标
        if parameters:
            cursor.execute(sql, parameters)
        else:
            cursor.execute(sql)
        # TODO: 查询完成之后，我们如何返回查询结果
        result_set = cursor.fetchall()
        for item in result_set:
            yield call_back(item)
    except Exception as exception:
        print(exception)
    finally:
        cursor.close()      # 关闭游标
        connect.close()     # 关闭数据库连接


def execute(sql, parameters=None):
    """
    执行更新（Update、Insert、Delete）
    :param sql: 要执行的更新语句
    :param parameters: 与更新语句对应的参数
    :return:
    """
    try:
        connect = get_connection()  # 创建数据库连接
        cursor = connect.cursor()  # 创建游标
        if parameters:
            cursor.execute(sql, parameters)
        else:
            cursor.execute(sql)
        connect.commit()
    except Exception as exception:
        print(exception)
    finally:
        cursor.close()  # 关闭游标
        connect.close()  # 关闭数据库连接


def execute_and_id(sql, parameters=None):
    """
    执行更新（Update、Insert、Delete）
    :param sql: 要执行的更新语句
    :param parameters: 与更新语句对应的参数
    :return:
    """
    try:
        connect = get_connection()  # 创建数据库连接
        cursor = connect.cursor()  # 创建游标
        if parameters:
            cursor.execute(sql, parameters)
        else:
            cursor.execute(sql)
        connect.commit()
        return cursor.lastrowid
    except Exception as exception:
        print(exception)
    finally:
        cursor.close()  # 关闭游标
        connect.close()  # 关闭数据库连接
