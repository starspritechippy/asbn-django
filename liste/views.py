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
    db_cursor.execute(
        "SELECT * FROM `asbn` ORDER BY `date` ASC, `time_start` ASC;"
    )
    zeilen = list(db_cursor)

    # step 1 Daten abfragen (nach anforderung?)
    # step 2 daten in template einbinden
    context = {
        "asbn_list": zeilen
    }
    db_conn.close()
    return HttpResponse(template.render(context, request))