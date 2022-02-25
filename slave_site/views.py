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
