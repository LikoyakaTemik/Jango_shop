from django.shortcuts import render

def index_page(request):
    context = {}
    return render(request,"index.html", context)
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
from django.shortcuts import render
import sqlite3 as sq
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
