# -*- coding:utf-8 -*-
import comm_sql as cmm

class Book(object):
    def __init__(self, bookname, author):
        self.bookname = bookname
        self.author = author

    def __str__(self):
        return "%s:%s" % (self.bookname, self.author)

sql = "Select bookname, author from books where author=%s or author=%s;"

books = cmm.query(sql, lambda item: Book(item[0], item[1]), ['余华', '高铭'])

for book in books:
    print(book)
