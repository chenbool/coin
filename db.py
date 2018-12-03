#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sqlite3

class Db(object):
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()
        pass

    # insert
    def ddl(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.rowcount
        self.close()
        return res

    # select
    def dml(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.close()
        return res

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    Db()