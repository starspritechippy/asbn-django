function todayISO() {
    const d = new Date(); 
    const iso = d.toISOString(); 
    return iso.substring(0, iso.indexOf('T'));
}

function absenden() {
    const datum                   = document.getElementById("datum");
    const datum_missing_error     = document.getElementById("datum_missing_error");
    const startzeit               = document.getElementById("startzeit");
    const startzeit_missing_error = document.getElementById("startzeit_missing_error");
    const endzeit                 = document.getElementById("endzeit");
    const endzeit_missing_error   = document.getElementById("endzeit_missing_error");
    const activity                = document.getElementById("activity");
    const activity_missing_error  = document.getElementById("activity_missing_error");
    const endzeit_time_error      = document.getElementById("endzeit_time_error");

    var absenden = true;

    if (!(datum.value)) {
        datum_missing_error.style = "display: block; color: red;"
        absenden = false;
    } else {
        datum_missing_error.style = "display: none; color: red;"
    }

    if (!(startzeit.value)) {
        startzeit_missing_error.style = "display: block; color: red;"
        absenden = false;
    } else {
        startzeit_missing_error.style = "display: none;"
    }

    if (!(endzeit.value)) {
        endzeit_missing_error.style = "display: block; color: red;"
        absenden = false;
    } else {
        endzeit_missing_error.style = "display: none;"
    }

    if (!(activity.value)) {
        activity_missing_error.style = "display: block; color: red;"
        absenden = false;
    } else {
        activity_missing_error.style = "display: none; color: red;"
    }

    if (endzeit.value && startzeit.value && endzeit.valueAsDate <= startzeit.valueAsDate) {
        endzeit_time_error.style = "display: block; color: red;"
        absenden = false;
    } else {
        endzeit_time_error.style = "display: none; color: red;"
    }

    return absenden;
}