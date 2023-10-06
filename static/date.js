function todayISO() {
    const d = new Date(); 
    const iso = d.toISOString(); 
    return iso.substring(0, iso.indexOf('T'));
}

// Source: https://weeknumber.com/how-to/javascript
// Returns the ISO week of the date.
Date.prototype.getWeek = function() {
    var date = new Date(this.getTime());
    date.setHours(0, 0, 0, 0);
    // Thursday in current week decides the year.
    date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
    // January 4 is always in week 1.
    var week1 = new Date(date.getFullYear(), 0, 4);
    // Adjust to Thursday in week 1 and count number of weeks from date to week1.
    return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
                          - 3 + (week1.getDay() + 6) % 7) / 7);
  }

function todayWeek() {
    const d = new Date();
    return d.getWeek();
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
        datum_missing_error.classList.add("has-error")
        absenden = false;
    } else {
        datum_missing_error.classList.remove("has-error")
    }

    if (!(startzeit.value)) {
        startzeit_missing_error.classList.add("has-error")
        absenden = false;
    } else {
        startzeit_missing_error.classList.remove("has-error")
    }

    if (!(endzeit.value)) {
        endzeit_missing_error.classList.add("has-error")
        absenden = false;
    } else {
        endzeit_missing_error.classList.remove("has-error")
    }

    if (!(activity.value)) {
        activity_missing_error.classList.add("has-error")
        absenden = false;
    } else {
        activity_missing_error.classList.remove("has-error")
    }

    if (endzeit.value && startzeit.value && endzeit.valueAsDate <= startzeit.valueAsDate) {
        endzeit_time_error.classList.add("has-error")
        absenden = false;
    } else {
        endzeit_time_error.classList.remove("has-error")
    }

    return absenden;
}

function checkIfInput(el) {
    console.log(el)
    if (!(el.value)) {
        el.classList.add("has-error")
    } else {
        el.classList.remove("has-error")
    }
}