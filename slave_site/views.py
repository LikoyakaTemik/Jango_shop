from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views import generic
from slave_site.forms import AddProductForm
from slave_site.models import Product


import sqlite3 as sq
id_user = 0
nickname = ["Anonymous"]
class Database_construction:
    @staticmethod
    def creating_tables(db):
        try:
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


def get_base_context(request):
    menu = [
        {"link": "/catalog/", "text": "Каталог"},
        {"link": "/new_product/", "text": "Добавить товар"},
    ]
    db = sq.connect("db.sqlite3")
    Database_construction.creating_tables(db)
    products = (db.execute("SELECT * FROM products")).fetchall()
    db.close()
    return {"menu": menu, "user": request.user, "products": products}

def adding_product(request):
    db = sq.connect("db.sqlite3")
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

def catalog_page(request):
    context = get_base_context(request)
    return render(request, "catalog.html", context)

def new_product(request):
    context = get_base_context(request)
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        form = AddProductForm(request.POST)
        label = form.data["label"]
        price = form.data["price"]
        url_img = form.data["url_img"]
        if form.is_valid():
            with db:
                arr =(label, price, url_img)
                db.execute("INSERT INTO products(label, price, url_img) VALUES(?, ?, ?)", arr)
            context["form"] = form
        return redirect("http://127.0.0.1:8000")

    else:
        form = AddProductForm()
        context["form"] = form
    db.close()
    return render(request, "new_product.html", context)


def enter(request):
    """display page of enter, executing of code of backend of log in"""
    db = sq.connect("db.sqlite3")
    Database_construction.creating_tables(db)
    ###подключение к БД
    if (request.method == "POST"):
        email = str(request.POST.get("exampleInputEmail1"))
        password = str(request.POST.get("exampleInputPassword1"))
        info = "nonclear"

        info = (db.execute("SELECT 'auth_user'.'email' FROM 'auth_user' WHERE ('auth_user'.'email'='" + email + "')")).fetchall()


        ##проверка на наличие ячейки
        if(info == []):
            print(info)
            print(email)
            print("NONE_EMAIL")
            db.close()
            return render(request, 'error.html') ##Нужно сделать
        else:
            truepassword = str(((db.execute("SELECT 'auth_user'.'password' from 'auth_user' WHERE ('auth_user'.'email'='" + email + "')")).fetchall())[0][0])
            if(truepassword == password):
                logging = ""
                if (email == "Anonymous"):
                    logging = "Войти"
                else:
                    logging = "Выйти"
                tranport_data = {"username": email, "logging": logging}
                nickname[0] = ((db.execute("SELECT 'auth_user'.'username' from 'auth_user' WHERE ('auth_user'.'email'='" + email + "')")).fetchall())[0][0]
                db.close()
                return redirect("http://127.0.0.1:8000", logging = "Выйти")
            else:
                db.close()
                print("FALSE_PASSWORD")
                return render(request, 'error.html')
            ###сравнивание: есл и пароли совпадают -> логин, иначе ошибка


    elif (request.method == "GET"):
        db.close()
        return render(request, 'login.html')


def registration(request):
    info = []
    db = sq.connect("db.sqlite3")
    Database_construction.creating_tables(db)

    if(request.method=="POST"):
        nick = request.POST.get("nick")
        pasw = request.POST.get("password")
        info = "nonclear"
        try:
            info = (db.execute("SELECT * FROM users WHERE nickname='" + request.POST.get("nick") + "'")).fetchall()
        except:
            pass

        if(info == []):
            pasw_res = ""

            for i in range(len(pasw)):
                if(ord(pasw[i]) >= 33):
                    pasw_res = pasw_res + chr(ord(pasw[i]) + 10)
            pasw = pasw_res

            try:
                db.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, nickname TEXT, password TEXT)")
            except:
                pass
            with db:
                db.execute("INSERT INTO users(nickname, password) VALUES ('" + nick + "', '" + pasw + "')")
                db.commit()
            db.close()
            return render(request, 'congratulateyou.html')
        else:
            db.close()
            return render(request, 'error.html')


    elif(request.method=="GET"):
        tranport_data = {"user": nickname[0]}
        db.close()
        return render(request, 'Registration.html', tranport_data)

def index_page(request):
    context = get_base_context(request)
    if request.method == "POST":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        db.close()
        return render(request, "index.html", context)
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        db.close()
        return render(request, "index.html", context)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
