function todayISO() {
    const d = new Date(); 
    const iso = d.toISOString(); 
    return iso.substring(0, iso.indexOf('T'));
}

function absenden() {
    const datum     = document.getElementById("datum");
    const startzeit = document.getElementById("startzeit");
    const endzeit   = document.getElementById("endzeit");
    const activity  = document.getElementById("activity");

    if (!(datum.value)) {
        alert("Datum fehlt.");
        return false;
    }

    if (!(startzeit.value)) {
        alert("Startzeit fehlt.");
        return false;
    }

    if (!(endzeit.value)) {
        alert("Endzeit fehlt.");
        return false;
    }

    if (!(activity.value)) {
        alert("Kommentar fehlt.");
        return false;
    }

    if (endzeit.valueAsDate <= startzeit.valueAsDate) {
        alert("Endzeit muss später als Startzeit sein.");
        return false;
    }

    return true;
}