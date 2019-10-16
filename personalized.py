# -*- coding:utf-8 -*-
"""
个性化商城首页
"""
from flask import Flask, render_template, session, redirect, url_for, request
import book_service as booksvc
import cart
import orders
import os
import recommand as rcmd

APP = Flask(__name__)
APP.register_blueprint(cart.shopping_cart, url_prefix="/cart")
APP.register_blueprint(orders.shopping_orders, url_prefix="/order")
APP.secret_key = os.urandom(38)

# 应用推荐矩阵
recommend_matrix = dict()
user_books = dict()
is_initialize = False


@APP.route("/login")
def login():
    return render_template("login.html")


@APP.route("/logout")
def logout():
    session.pop("user_id")  # 从session中删除user_id项
    return redirect("/")


@APP.route("/do_login", methods=["POST"])
def do_login():
    data = request.get_data().decode()
    user_name_password = data.split("&")
    user_name = user_name_password[0].split("=")[1]
    password = user_name_password[1].split("=")[1]
    # 拿着获取到的用户名和密码进行登录
    user_id = booksvc.UserService.login(user_name, password)
    if user_id:
        session.setdefault("user_id", user_id)
    return redirect("/")


# 该路由匹配http://localhost:5000/0，后面带page参数
@APP.route("/<int:page>")
# 该路由匹配http://localhost:5000，不带参数
@APP.route("/")
def index(page=0):
    if not session.get("user_id"):
        return redirect("/login")
    boksvc = booksvc.BookService()
    recommend_books = boksvc.get_recommend_books(rcmd.recommend(user_books[session.get("user_id")], recommend_matrix))
    books, hasNext = boksvc.get_all_book(page)
    return render_template("index.html", my_books=books, has_next=hasNext, page_index=page,
                           recommend_books=recommend_books)


@APP.route("/detail/<id>")
def detail(id):
    return render_template("detail.html", bookid=id)


if __name__ == "__main__":
    user_books = booksvc.UserService.get_books_by_user()
    recommend_matrix = rcmd.build_martix(user_books)
    is_initialize = True
    APP.run(debug=True)
