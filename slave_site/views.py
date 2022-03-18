from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
import sqlite3 as sq
id_user = 0
class Database_construction:
    @staticmethod
    def creating_tables(db):
        try:
            db.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " nickname TEXT,"
                       " mail TEXT,"
                       " password TEXT)")
            db.execute("CREATE TABLE products(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " label TEXT,"
                       " likes INTEGER,"
                       " id_category TEXT,"
                       " price INTEGER, "
                       " url_img TEXT)")
            db.execute("CREATE TABLE users_products(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " id_product INTEGER,"
                       " id_user INTEGER)")
            db.execute("CREATE TABLE categories(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "name TEXT)")
            db.execute("CREATE TABLE likes(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " id_user INTEGER,"
                       " id_category INTEGER,"
                       " amount INTEGER)")
            db.execute("CREATE TABLE shopping_cart(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " id_user INTEGER,"
                       " id_product INTEGER,"
                       " amount INTEGER)")
        except:
            print("Таблицы уже созданы!")
def index_page(request):
    db = sq.connect("DB")
    Database_construction.creating_tables(db)
    db.close()
    return render(request,"Main_page.html")


def adding_product(request):
    db = sq.connect("DB")
    Database_construction.creating_tables(db)
    if request.method == "POST":
        id_product = int(request.POST.get('id'))
        ammo = (db.execute("SELECT amount FROM shopping_cart WHERE id_user=" + id_user + " AND id_product=" + id_product)).fetchall()
        if(len(ammo) == 0):
            with db:
                db.execute("INSERT INTO shopping_cart(id_user, id_product, amount)"
                           " VALUES(" + id_user + ", " + id_product + ", 1)")
        else:
            ammo = ammo[0][0] + 1
            with db:
                db.execute("UPDATE shopping_cart SET amount=" + ammo + " WHERE id_user=" + id_user + " AND id_product=" + id_product)
    db.close()
    return JsonResponse()