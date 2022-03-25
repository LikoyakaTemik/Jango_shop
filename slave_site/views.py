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
  
def get_base_context(request):
    menu = [
        {"link": "/catalog/", "text": "Каталог"},
    ]

    return {"menu": menu, "user": request.user}

def catalog_page(request):
    context = get_base_context(request)
    return render(request, "catalog.html", context)



def enter(request):
    """display page of enter, executing of code of backend of log in"""
    database = sq.connect("mesbase.sqlite3", timeout=10)
    try:
        database.execute(
            "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, nickname TEXT, password TEXT)")
    except:
        pass
    ###подключение к БД
    if (request.method == "POST"):
        nick = request.POST.get("nick")###вместо nick название атрибута name тега input
        password = str(request.POST.get("password")) ###вместо paswword название атрибута name тега input
        info = "nonclear"
        try:
            info = (database.execute("SELECT nickname FROM users WHERE nickname='" + nick + "'")).fetchall()
        except:
            pass
        ##проверка на наличие ячейки
        if(info == []):
            database.close()
            return render(request, 'errorpas.html')
        else:
            truepassword = ((database.execute("SELECT password from users WHERE nickname='" + nick + "'")).fetchall())[0][0]
            truepasw_res = ""
            ###запрос шифрованного пароля из БД
            for i in range(len(truepassword)):
                truepasw_res = truepasw_res + chr(ord(truepassword[i]) - 10)
            truepassword = truepasw_res
            ###расшифровка пароля
            if(truepassword == password):
                logging = ""
                if (nick == "Anonymous"):
                    logging = "Войти"
                else:
                    logging = "Выйти"
                tranport_data = {"user": nick, "logging": logging}
                nickname[0] = nick
                database.close()

                return redirect("http://127.0.0.1:8000", logging = "Выйти")
            else:
                database.close()
                return render(request, 'errorpas.html')
            ###сравнивание: если пароли совпадают -> логин, иначе ошибка


    elif (request.method == "GET"):
        database.close()
        return render(request, 'login.html')


def registration(request):
    database = sq.connect("mesbase.sqlite3", timeout=10)
    info = []
    try:
        database.execute(
            "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, nickname TEXT, password TEXT)")
    except:
        pass

    if(request.method=="POST"):
        nick = request.POST.get("nick")
        pasw = request.POST.get("password")
        info = "nonclear"
        try:
            info = (database.execute("SELECT * FROM users WHERE nickname='" + request.POST.get("nick") + "'")).fetchall()
        except:
            pass

        if(info == []):
            pasw_res = ""

            for i in range(len(pasw)):
                if(ord(pasw[i]) >= 33):
                    pasw_res = pasw_res + chr(ord(pasw[i]) + 10)
            pasw = pasw_res

            try:
                database.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, nickname TEXT, password TEXT)")
            except:
                pass
            with database:
                database.execute("INSERT INTO users(nickname, password) VALUES ('" + nick + "', '" + pasw + "')")
                database.commit()
            database.close()
            return render(request, 'congratulateyou.html')
        else:
            database.close()
            return render(request, 'error.html')


    elif(request.method=="GET"):
        tranport_data = {"user": nickname[0]}
        database.close()
        return render(request, 'Registration.html', tranport_data)

def index_page(request):
    db = sq.connect("DB")
    Database_construction.creating_tables(db)
    db.close()
    return render(request,"Main_page.html")

