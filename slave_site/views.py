from django.shortcuts import render

def index_page(request):
    context = {}
    
    return render(request,"index.html", context)

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