export function dateToString(date) {
    var dateReturn =
        date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
    return dateReturn;
}

export var monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];
