# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, abort, session, redirect, request
from jinja2 import TemplateNotFound
from book_service import CartService, OrderService

shopping_orders = Blueprint("orders", __name__, static_folder="static", template_folder="templates")


@shopping_orders.route("/index")
def index():
    user_id = session.get("user_id")  # 从session中取出键值为user_id的用户信息
    # 如果没有取到用户id，说明当前用户并没有登录，跳转到登录页
    if not user_id:
        return redirect("/login")
    else:
        return render_template("order.html", details=OrderService.get_orders_by_user(user_id))
