# -*- coding:utf-8 -*-
"""
用来处理用户登录
"""
from flask import Blueprint, render_template, abort, session, redirect

login_service = Blueprint("login", __name__, static_folder="static", template_folder="templates")


@login_service.route("/")
def login():
    return render_template("login.html")
