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

    if (date_from := request.GET.get("date_from")) and (date_to := request.GET.get("date_to")):
        if date_from == date_to:
            db_cursor.execute("SELECT * FROM `asbn` WHERE `date` = ? ORDER BY `time_start` ASC;", [date_from])
        else:
            db_cursor.execute("SELECT * FROM `asbn` WHERE `date` BETWEEN ? AND ? ORDER BY `date` ASC, `time_start` ASC;", [date_from, date_to])
    
    elif kw := request.GET.get("date_kw"):
        db_cursor.execute("SELECT * FROM `asbn` WHERE WEEK(`date`) = ? ORDER BY `date` ASC, `time_start` ASC;", [kw])
    
    else:
        db_cursor.execute("SELECT * FROM `asbn` ORDER BY `date` ASC, `time_start` ASC;")
    result = db_cursor.fetchall()
    db_conn.close()

    asbn_list = []
    date = ""
    entries = []
    for row in result:
        if row["date"] != date:
            if entries:
                asbn_list.append(entries)
                entries = []
            date = row["date"]
        entries.append(row)

    if entries:
        asbn_list.append(entries)

    context = {
        "asbn_list": asbn_list
    }
    return HttpResponse(template.render(context, request))