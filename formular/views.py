import os
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader
from django.shortcuts import redirect

import mariadb
from dotenv import load_dotenv

def index(request):
    template = loader.get_template("formular/template.html")
    context = {}
    if request.GET.get("error", ""):
        context["error"] = True
        detailed_error = request.GET.get("errors")
        missing = detailed_error.split(",")
        for item in missing:
            context[item] = True
    elif request.GET.get("success"):
        context["success"] = True
    return HttpResponse(template.render(context, request))

def send_form(request):
    datum     = request.POST.get("datum")
    startzeit = request.POST.get("startzeit")
    endzeit   = request.POST.get("endzeit")
    activity  = request.POST.get("activity")

    if not datum or not startzeit or not endzeit or not activity:
        redirect_params = []
        if not datum:
            redirect_params.append("missing_datum")
        if not startzeit:
            redirect_params.append("missing_startzeit")
        if not endzeit:
            redirect_params.append("missing_endzeit")
        if not activity:
            redirect_params.append("missing_activity")

        redirect_url = "/formular/?error=1&errors=" + ",".join(redirect_params)
        # z.B. ?error=1&errors=missing_datum,missing_startzeit,missing_activity
        return redirect(redirect_url)
    
    load_dotenv()

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
    
    db_cursor = db_conn.cursor()
    db_cursor.execute(
        "INSERT INTO `asbn` (date, time_start, time_end, activity) VALUES (?, ?, ?, ?)", 
        (datum, startzeit, endzeit, activity)
    )

    return redirect("/formular/?success=1")