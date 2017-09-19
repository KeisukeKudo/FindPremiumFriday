from calendar import monthrange
from datetime import datetime, timedelta
from flask import Flask

api = Flask(__name__)

YEAR_POSITION = 0
MONTH_POSITION = 1


@api.route('/premium-friday')
def current_month_premium_friday():
    current_date = list(map(int, datetime.now().strftime('%Y,%m').split(',')))
    year = current_date[YEAR_POSITION]
    month = current_date[MONTH_POSITION]

    last_date, weekday = last_date_weekday(year, month)

    return find_premium_friday(last_date, weekday)


@api.route('/premium-friday/<int:year>/<int:month>', methods=['POST'])
def parameter_find_premium_friday(year, month):
    try:
        last_date, weekday = last_date_weekday(year, month)

        return find_premium_friday(last_date, weekday)
    except ValueError:
        return 404


def find_premium_friday(last_date, weekday):

    while weekday > -2:
        if weekday == 4:
            break

        if weekday == -1:
            weekday += 7

        last_date -= timedelta(days=1)
        weekday -= 1

    return last_date.strftime('%Y-%m-%d')


def last_date_weekday(year, month):
    last_date = datetime(year, month, monthrange(year, month)[MONTH_POSITION])
    weekday = last_date.weekday()

    return last_date, weekday


if __name__ == '__main__':
    api.run()
