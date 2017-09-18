from calendar import monthrange
from datetime import datetime, timedelta
from flask import Flask

api = Flask(__name__)


@api.route('/premium-friday')
def current_month_premium_friday():
    current_date = list(map(int, datetime.now().strftime('%Y,%m').split(',')))
    year = current_date[0]
    month = current_date[1]

    last_date = datetime(year, month, monthrange(year, month)[1])
    weekday = last_date.weekday()

    return find_premium_friday(last_date, weekday)


@api.route('/premium-friday/<int:year>/<int:month>', methods=['POST'])
def parameter_find_premium_friday(year, month):
    try:
        last_date = datetime(year, month, monthrange(year, month)[1])
        weekday = last_date.weekday()
        return find_premium_friday(last_date, weekday)

    except ValueError:
        return 404


def find_premium_friday(last_date, weekday):
    for i in reversed(range(1, 8)):
        if weekday == 3:
            break

        if weekday == 0:
            weekday += 6

        last_date -= timedelta(days=1)
        weekday -= 1

    return last_date.strftime('%Y-%m-%d')


if __name__ == '__main__':
    api.run()
