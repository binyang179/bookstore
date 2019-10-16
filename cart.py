# -*- coding:utf-8 -*-
"""
购物车模块
"""
from flask import Blueprint, render_template, abort, session, redirect, request
from jinja2 import TemplateNotFound
from book_service import CartService, OrderService

shopping_cart = Blueprint("cart", __name__, static_folder="static", template_folder="templates")


@shopping_cart.route("/index")
def index():
    user_id = session.get("user_id")  # 从session中取出键值为user_id的用户信息
    # 如果没有取到用户id，说明当前用户并没有登录，跳转到登录页
    if not user_id:
        return redirect("/login")
    else:
        return render_template("cart.html", books=CartService.get_carts_by_user(user_id))


@shopping_cart.route("/<id>")
def add_2_cart(id):
    """
    将物品编号是id的物品放入到用户购物车
    :param id:
    :return:
    """
    try:
        user_id = session.get("user_id")  # 从session中取出键值为user_id的用户信息
        # 如果没有取到用户id，说明当前用户并没有登录，跳转到登录页
        if not user_id:
            return redirect("/login")
        else:
            CartService.add_2_cart(user_id, id)
            return redirect("/cart/index")
    except TemplateNotFound:
        abort(404)


@shopping_cart.route("/<id>/remove")
def remove_from_cart(id):
    try:
        user_id = session.get("user_id")
        CartService.remove_from_carts(user_id, id)
        return redirect("/cart/index")
    except Exception as exception:
        abort(500)


@shopping_cart.route("/add2order", methods=["GET", "POST"])
def add_2_order():
    user_id = session.get("user_id")
    book_counts = []
    for key, value in request.form.items():
        print(key)
        book_id = key.split("_")[1]
        cart_id = key.split("_")[2]
        book_count = value
        book_counts.append((book_id, book_count, cart_id))
    OrderService.add_2_order(user_id, book_counts)
    return redirect("/order/index")
