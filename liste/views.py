import os
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.template import loader
import mariadb

def index(request):
    template = loader.get_template("liste/template.html")

    try:
        db_conn = mariadb.connect(
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASS"),
            host = os.getenv("DB_HOST"),
            port = int(os.getenv("DB_PORT")),
            database = os.getenv("DB_NAME")
        )
    except mariadb.Error as e:
        return HttpResponseServerError(f"Fehler beim verbinden mit der Datenbank: {e}")
    
    db_cursor = db_conn.cursor(dictionary=True)

    if kw := request.GET.get("kw"):
        print(kw)
        db_cursor.execute("SELECT * FROM `asbn` WHERE WEEK(`date`) = ? ORDER BY `date` ASC, `time_start` ASC;", [kw])
    else:
        db_cursor.execute("SELECT * FROM `asbn` ORDER BY `date` ASC, `time_start` ASC;")
    zeilen = db_cursor.fetchall()

    daten = []
    date = ""
    entries = []
    for zeile in zeilen:
        if zeile["date"] != date:
            if entries:
                daten.append(entries)
                entries = []
            date = zeile["date"]
        entries.append(zeile)

    if entries:
        daten.append(entries)

    # step 1 Daten abfragen (nach anforderung?)
    # step 2 daten in template einbinden
    context = {
        "asbn_list": daten
    }
    db_conn.close()
    return HttpResponse(template.render(context, request))