from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .forms import AddProductForm
from .models import Product
from .forms import ChatInputForm
from .forms import AddToCartForm
from .forms import CreateChatForm
from .forms import ChatOutputForm
# Создаем здесь представления.

import sqlite3 as sq
class Database_construction:
    @staticmethod
    def creating_tables(db):
        try:
            db.execute("CREATE TABLE products(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " label TEXT,"
                       " likes INTEGER,"
                       " id_category TEXT,"
                       " price INTEGER, "
                       " username TEXT, "
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
        except:
            print("Таблицы уже созданы!")

def get_base_context(request, receiver):
    menu = [
        {"link": "/chat_list/", "text": "Чаты"},
        {"link": "/shopping_cart/", "text": "Корзина"},
        {"link": "/new_product/", "text": "Добавить товар"},
    ]
    db = sq.connect("db.sqlite3")
    Database_construction.creating_tables(db)
    products = (db.execute("SELECT * FROM products")).fetchall()

    if str(request.user) != "AnonymousUser":
        username = str(request.user)
        id_username = "Error"
        try:
            id_username = (db.execute("SELECT id FROM auth_user WHERE username = " + username).fetchall())[0][0]
        except:
            id_username = "Error"
        if id_username != "Error":
            chat = db.execute("SELECT * FROM chat WHERE id_receiver = " + id_username).fetchall()
            messages = []
            for i in len(chat):
                mes = db.execute("SELECT * FROM messages WHERE id_chat = " + chat[i][0]).fetchall()
                messages.append(mes)
            if receiver != "Anonuser":
                tr_data = db.execute("SELECT id FROM chat WHERE receiver = ?", (username,)).fetchall()
                tr_data2 = db.execute("SELECT sender FROM chat WHERE receiver = ?", (username,)).fetchall()
                for i in range(len(tr_data)):
                    id_chat = tr_data[i]
                for i in range(len(tr_data2)):
                    senders = tr_data2[i]
                messages = db.execute("SELECT * FROM messages WHERE id_chat = ?", id_chat).fetchall()
                return {"messages": messages}
        else:
            chat = {("No login in base")}
    else:
        chat = {("Login to have chats")}
    db.close()
    return {"menu": menu, "user": request.user, "products": products, "chat": chat}

def create_chat(request):
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        form = CreateChatForm(request.POST)
        username = str(request.user)
        with db:
                id_receiver = (db.execute("SELECT id FROM auth_user WHERE username = " + username)).fetchall()[0]

            db.execute("INSERT INTO chat(id_receiver) VALUES(?)", id_receiver)
    db.close()
    return render(request, "chat_list.html")

def chat_input(request):
    context = get_base_context(request, "AnonymousUser")
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        form = ChatInputForm(request.POST)
        username = str(request.user)
        message = form.data["mes"]
        if form.is_valid():
            with db:
                id_sender = db.execute("SELECT id FROM auth_user WHERE username = " + username).fetchall()[0]
                
            context["form"] = form
    else:
        form = ChatInputForm()
        context["form"] = form
    db.close()
    return redirect("https://servusmarket.herokuapp.com/room")

"""def chat_output(request, receiver):
    context = get_base_context(request)
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        username = str(request.user)
        print(1)
        with db:
            arr = (username, receiver)
            messages = db.execute("SELECT * FROM messages WHERE username = ? AND receiver = ?", arr).fetchall()
            print(messages)
    db.close()
    return render(request, "room.html", {"messages": messages})"""

def chat_list(request):
    context = get_base_context(request, "Anonuser")
    if request.method == "POST":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        db.close()
        return render(request, "chat_list.html", context)
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        db.close()
        return render(request, "chat_list.html", context)

def room(request):
    if request.method == "POST":
        """
        receiver = request.POST.get('username')
        context = get_base_context(request, receiver)
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        db.close()
        """
        return redirect("https://servusmarket.herokuapp.com")
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        db.close()
        return render(request, "room.html")

def home(request):
    context = get_base_context(request, "Anonuser")
    if request.method == "POST":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        db.close()
        return render(request, "home.html", context)
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        db.close()
        return render(request, "home.html", context)

def shopping_cart(request):
    context = get_base_context(request, "AnonymousUser")
    if request.method == "POST":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        main_username = str(request.user)
        id_product = db.execute("SELECT id_product FROM shopping_cart WHERE main_username = ?",
                                (main_username,)).fetchall()
        if len(id_product) == 0:
            return render(request, "shopping_cart.html")
        else:
            shopping_cart = []
            for i in range(len(id_product)):
                product = (db.execute("SELECT * FROM products WHERE id = ?", id_product[i]).fetchall())[0]
                shopping_cart.append(product)
            db.close()
            return render(request, "shopping_cart.html", {"shopping_cart": shopping_cart})
    elif request.method == "GET":
        db = sq.connect("db.sqlite3")
        Database_construction.creating_tables(db)
        main_username = str(request.user)
        id_product = db.execute("SELECT id_product FROM shopping_cart WHERE main_username = ?",
                                (main_username,)).fetchall()
        if len(id_product) == 0:
            return render(request, "shopping_cart.html")
        else:
            shopping_cart = []
            for i in range(len(id_product)):
                product = (db.execute("SELECT * FROM products WHERE id = ?", id_product[i]).fetchall())[0]
                shopping_cart.append(product)
            db.close()
            return render(request, "shopping_cart.html", {"shopping_cart": shopping_cart})

def add_sc(request):
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        main_username = str(request.user)
        username = str(form.data["username"])
        with db:
            tr_data = db.execute("SELECT id FROM products WHERE username = ?", (username,)).fetchall()
            id_product = egor_letov(tr_data)
            arr = (id_product, main_username, username)
            db.execute("INSERT INTO shopping_cart(id_product, main_username, username) VALUES(?, ?, ?)", arr)
        db.close()
        return redirect("https://servusmarket.herokuapp.com")

def egor_letov(list):
    print(list)
    tuple = list[0]
    object = tuple[0]
    return object

def new_product(request):
    context = get_base_context(request, "Anonuser")
    db = sq.connect("db.sqlite3")
    if request.method == "POST":
        form = AddProductForm(request.POST)
        label = form.data["label"]
        price = form.data["price"]
        url_img = form.data["url_img"]
        user = str(request.user)
        likes = 0
        id_category = form.data["category"]
        if form.is_valid():
            with db:
                arr = (label,likes,id_category, price, url_img, user)
                db.execute("INSERT INTO products(label, likes, id_category, price, url_img, username) VALUES(?, ?, ?, ?, ?, ?)", arr)
            context["form"] = form
        return redirect("https://servusmarket.herokuapp.com")

    else:
        form = AddProductForm()
        context["form"] = form
    db.close()
    return render(request, "new_product.html", context)

def account(request):
    context = get_base_context(request, "Anonuser")
    return render(request, "account.html", context)

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
