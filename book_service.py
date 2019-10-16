# -*- coding:utf-8 -*-
"""
处理针对图书的一组操作
"""
import comm_sql as cmsql
import datetime as dt


class Book(object):
    """
    图书信息
    """

    def __init__(self, id, author, bookname, image, unitprice, publisher, publishedOn, discount):
        self.id = id
        self.author = author
        self.book_name = bookname
        self.image_url = image,
        self.unit_price = unitprice
        self.publisher = publisher
        self.publishedOn = publishedOn
        self.discount = discount


class BookService(object):
    """
    图书操作
    """

    def __init__(self):
        pass

    @staticmethod
    def build_book_item(result_item):
        """
        从result_item中构建一个book对象
        :param result_item: cursor对象
        :return:
        """
        book = Book(result_item[0],
                    result_item[1],
                    result_item[2],
                    result_item[3],
                    result_item[4],
                    result_item[5],
                    result_item[6],
                    result_item[7])
        return book

    def get_all_book(self, page=0, size=39):
        """
        根据当前的页码和每页的条数，获取接下来的数据条数
        :param page: 当前页码，从0开始，0表示第一页
        :param size: 每页的数据条数，默认是40，即每页显示40条
        :return: 图书列表，是否还有下一页图书信息
        """
        counts = cmsql.query("Select count(1) from books", lambda x: int(x[0]))
        for c in counts:
            count = c
        query = "Select idbooks, Author, bookname, image_url, unitprice, publisher, publishedOn, discount from books limit %s offset %s;"
        # 计算开始的条数
        start = page * size
        books = cmsql.query(query, self.build_book_item, [size, start])
        return books, start + size < count

    def get_recommend_books(self, books):
        result = []
        query = "Select idbooks, Author, bookname, image_url, unitprice, publisher, publishedOn, discount from books where idbooks=%s"
        for book_id in books:
            books = cmsql.query(query, self.build_book_item, [book_id])
            for book in books:
                result.append(book)
        return result


class CartService(object):
    """
    购物车服务类，用于操作购物车相关的数据操作
    """

    @staticmethod
    def add_2_cart(userid, bookId):
        """
        将用户选定的图书添加到用户的购物车中
        :param userid:用户编号
        :param bookId:图书编号
        :return:
        """
        query = "Insert Into shoppingcarts(user_id, book_id)values(%s, %s)"
        cmsql.execute(query, [userid, bookId])

    @staticmethod
    def get_carts_by_user(user_id):
        """
        获取指定用户的购物车信息
        :param user_id:用户编号
        :return:
        """
        query = "select idbooks,bookname, image_url, unitprice, idcarts From books inner join shoppingcarts on shoppingcarts.book_id=books.idbooks where shoppingcarts.user_id=%s"
        books = cmsql.query(query, lambda cur: (cur[0], cur[1], cur[2], cur[3], cur[4]), [user_id])
        return books

    @staticmethod
    def remove_from_carts(user_id, book_id):
        """
        从购物车中删除指定用户的指定商品
        :param user_id: 用户编号
        :param book_id: 图书编号
        :return:
        """
        query = "Delete From shoppingcarts where user_id=%s and book_id=%s"
        cmsql.execute(query, [user_id, book_id])


class OrderService(object):
    @staticmethod
    def get_orders_by_user(user_id):
        """
        根据用户编号查询对应的订单信息
        :param user_id: 用户编号
        :return: 订单列表
        """
        sql = "Select idorders from orders where user_id=%s"
        orders = cmsql.query(sql, lambda x: x[0], [user_id])
        detail_query = "Select bookname,unitprice,image_url from order_view where order_id=%s"
        result = dict()
        for order in orders:
            result[order] = list()
            details = cmsql.query(detail_query, lambda x: (x[0], x[1], x[2]), [order])
            for detail in details:
                result[order].append(detail)
        return result

    @staticmethod
    def add_2_order(user_id, books_count):
        # 1. 创建一个order
        query = "Insert Into Orders(user_id, order_date, total_price)values(%s,%s,%s);"
        order_id = cmsql.execute_and_id(query, [user_id, dt.datetime.now(), 0])
        # 2. 创建一个order_detail
        query = "Insert Into Order_Details(order_id, book_id, order_count)values(%s,%s,%s)"
        remove_query = "Delete from shoppingcarts where idcarts=%s"
        for book_count in books_count:
            cmsql.execute(query, [order_id, book_count[0], book_count[1]])
            # 3. 从购物车中删除对应的数据
            cmsql.execute(remove_query, [book_count[2]])


class UserService(object):
    @staticmethod
    def login(user_name, password):
        current_user_id = None
        query = "Select idusers from users where user_name=%s and password=%s"
        user_count = cmsql.query(query, lambda cnt: int(cnt[0]), [user_name, password])
        for c in user_count:
            current_user_id = c
        return current_user_id

    @staticmethod
    def get_books_by_user():
        result = dict()
        query = "Select idusers from users"
        user_ids = [user_id for user_id in cmsql.query(query, lambda x: x[0])]
        select_book_query = "Select idbooks from order_view where user_id=%s"
        for uid in user_ids:
            result[uid] = list()
            books = cmsql.query(select_book_query, lambda x: x[0], [uid])
            for book in books:
                result[uid].append(book)
        return result
