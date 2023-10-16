import datetime
import os
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.template import loader
import mariadb
from pypdf import PdfReader, PdfWriter
from io import BytesIO


def kw_from_date(date: datetime.date | datetime.datetime | str) -> int:
    if isinstance(date, datetime.datetime):
        date = date.date()
    elif isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    date_kw = date.isocalendar().week
    return date_kw

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
            db_cursor.execute("SELECT *, WEEK(`date`) AS kw FROM `asbn` WHERE `date` = ? ORDER BY `time_start` ASC;", [date_from])
        else:
            db_cursor.execute("SELECT *, WEEK(`date`) AS kw FROM `asbn` WHERE `date` BETWEEN ? AND ? ORDER BY `date` ASC, `time_start` ASC;", [date_from, date_to])
    
    elif kw := request.GET.get("date_kw"):
        db_cursor.execute("SELECT *, WEEK(`date`) AS kw FROM `asbn` WHERE WEEK(`date`) = ? ORDER BY `date` ASC, `time_start` ASC;", [kw])
    
    else:
        db_cursor.execute("SELECT *, WEEK(`date`) AS kw FROM `asbn` ORDER BY `date` ASC, `time_start` ASC;")
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
        "asbn_list": asbn_list,
        "date_from": request.GET.get("date_from"),
        "date_to": request.GET.get("date_to"),
        "date_kw": request.GET.get("date_kw"),
    }
    return HttpResponse(template.render(context, request))


def pdf_gen(request):
    date_kw = request.GET.get("date_kw")
    date_from = request.GET.get("date_from")

    if not date_kw:
        if not date_from:
            return HttpResponseServerError("Bitte KW oder Startdatum angeben!")
        else:
            week_filter = kw_from_date(date_from)
    else:
        week_filter = int(date_kw)

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
    db_cursor.execute("SELECT *, WEEK(`date`) AS kw, WEEKDAY(`date`) + 1 as dow FROM `asbn` WHERE WEEK(`date`) = ? ORDER BY `date` ASC, `time_start` ASC;", [week_filter])
    result = db_cursor.fetchall()
    db_conn.close()

    asbn_list = []
    dow = 0
    entries = []
    for row in result:
        if row["dow"] != dow:
            if entries:
                asbn_list.append(entries)
                entries = []
            dow = row["dow"]
        entries.append(row)

    if entries:
        asbn_list.append(entries)

    if len(asbn_list) < 5:
        return HttpResponseServerError(f"Einträge für KW {week_filter} unvollständig!")
    # TODO auch unvollständige ASBN sollten ausgegeben werden können

    activities = {
        "day1": "\n".join(row["activity"] for row in asbn_list[0]),
        "day2": "\n".join(row["activity"] for row in asbn_list[1]),
        "day3": "\n".join(row["activity"] for row in asbn_list[2]),
        "day4": "\n".join(row["activity"] for row in asbn_list[3]),
        "day5": "\n".join(row["activity"] for row in asbn_list[4]),
    }

    reader = PdfReader("Vorlage_ASBN.pdf")
    writer = PdfWriter()

    writer.append(reader)
    writer.update_page_form_field_values(
        writer.pages[0],
        {
            "Ausbildungsjahr_es_:sender":                "2023/2024",
            "Azubi_Name_es_:sender:fullname":            "Maximilian Heymann",
            "Azubi_Unterschrift_Datum_es_:sender:date":  datetime.date.today().isoformat(),
            # "Begleiter_Name_es_:fullname":               "Alexander Clermont",
            # "Begleiter_Unterschrift_Datum_es_:date":     datetime.date.today().isoformat(),
            "Dropdown13_es_:sender:signatureblock":      "Fachinformatiker für Anwendungsentwicklung",
            "Kalenderwoche_es_:sender":                  str(week_filter),
            # "Klassenlehrer_Name_es_:fullname":           "Wittkopf",
            # "Klassenlehrer_Unterschrift_Datum_es_:date": "2023-10-16",
            "Tag1_Datum_es_:sender:date":                asbn_list[0][0].get("date"),
            "Tag1_Lernort_es_:sender":                   "Betrieb",
            "Tag1_Stunden_es_:sender":                   "7,6",  # TODO 7,6 Stunden annehmen OK, aber für Urlaub, Krank, Feiertag falsch
            "Tag1_Tätigkeiten_es_:sender":               activities["day1"],
            "Tag2_Datum_es_:sender:date":                asbn_list[1][0].get("date"),
            "Tag2_Ort_es_:sender":                       "Betrieb",
            "Tag2_Stunden_es_:sender":                   "7,6",
            "Tag2_Tätigkeiten_es_:sender":               activities["day2"],
            "Tag3_Datum_es_:sender:date":                asbn_list[2][0].get("date"),
            "Tag3_Ort_es_:sender":                       "Betrieb",
            "Tag3_Stunden_es_:sender":                   "7,6",
            "Tag3_Tätigkeiten_es_:sender":               activities["day3"],
            "Tag4_Datum_es_:sender":                     asbn_list[3][0].get("date"),
            "Tag4_Ort_es_:sender":                       "Betrieb",
            "Tag4_Stunden_es_:sender":                   "7,6",
            "Tag4_Tätigkeiten_es_:sender":               activities["day4"],
            "Tag5_Datum_es_:sender":                     asbn_list[4][0].get("date"),
            "Tag5_Ort_es_:sender":                       "Betrieb",
            "Tag5_Stunden_es_:sender":                   "7,6",
            "Tag5_Tätigkeiten_es_:sender":               activities["day5"],
            "Zeitraum_es_:sender:date":                  f"{asbn_list[0][0].get('date')}  -  {asbn_list[4][0].get('date')}",
        },
    )

    xfile = BytesIO()
    writer.write(xfile)

    xfile.seek(0)
    contents = xfile.read()
    return HttpResponse(contents, content_type="application/pdf")