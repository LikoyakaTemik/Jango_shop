from django.shortcuts import render
import sqlite3 as sq
db = sq.connect("DB")
class Database_construction:
    @staticmethod
    def creating_tables():
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
    context = {}
    
    return render(request,"index.html", context)
