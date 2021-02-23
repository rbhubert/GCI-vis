import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


# Returns a datatime value from the string _date_
def twitter_format(date):
    return datetime.datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')


# Returns each date between date1 and date2
def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


# Returns each date and hours between date1 and date2
def daterange_hours(date1, date2):
    diff = date2 - date1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600

    for h in range(1, hours):
        yield date1 + timedelta(hours=h)


# Returns the datetime from a str with minutes/hours/days ago in its format.
def get_past_date(creation_date, str_days_ago):
    TODAY = datetime.datetime.today()
    splitted = str_days_ago.split()
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return creation_date
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = TODAY - relativedelta(days=1)
        return date
    elif splitted[1].lower() in ['minutes', 'min', 'm']:
        date = datetime.datetime.now() - relativedelta(minutes=int(splitted[0]))
        return date
    elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
        return date
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = TODAY - relativedelta(days=int(splitted[0]))
        return date
    elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
        date = TODAY - relativedelta(weeks=int(splitted[0]))
        return date
    elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
        date = TODAY - relativedelta(months=int(splitted[0]))
        return date
    elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
        date = TODAY - relativedelta(years=int(splitted[0]))
        return date
    else:
        return "Wrong Argument format"
