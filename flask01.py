from flask import Flask, request, render_template
import psycopg2
import datetime
import platform
import sys

app = Flask(__name__)


def calculate_period_1_epics():
    total = 0
    small_total = 0
    medium_total = 0
    large_total = 0
    xl_total = 0
    epics = {}
    hostname = 'localhost'
    username = 'predictuser'
    password = 'password'
    database = 'predictatron'
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cur = conn.cursor()
    cur.execute("SELECT epic_id, snapshot_date, goal_period, epic_title, status, kanban_small, kanban_medium, kanban_large, kanban_xl FROM epic WHERE goal_period=1")
    for epic_id_x, snapshot_date_x, goal_period_x, epic_title_x, status_x, kanban_small_x, kanban_medium_x, kanban_large_x, kanban_xl_x in cur.fetchall():
        epics[epic_id_x] = {'snapshot_date': snapshot_date_x, 'goal_period': goal_period_x, 'epic_title': epic_title_x,
                            'status': status_x, 'kanban_small': kanban_small_x, 'kanban_medium': kanban_medium_x,
                            'kanban_large': kanban_large_x, 'kanban_xl': kanban_xl_x}
        small_total += kanban_small_x
        medium_total += kanban_medium_x
        large_total += kanban_large_x
        xl_total += kanban_xl_x
    conn.close()
    total = (small_total*5) + (medium_total * 8) + (large_total * 13) + (xl_total * 21)
    return total


def extra_stuff():
    return " - database successfully accessed"


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/dash')
@app.route('/dash/<multiplier>')
@app.route('/dash/<multiplier>/<snapshotdate>')
def dash(multiplier=1.5, snapshotdate='2017-06-06'):

    snapshot_date = datetime.datetime.now().time()
    snapshot_name = "Undefined"
    backlog_small = 0  # 121
    backlog_medium = 0  # 81
    backlog_large = 0  # 26
    backlog_xl = 0  # 9
    history_weeks = 0  # 24
    history_small = 0  # 33
    history_medium = 0  # 12
    history_large = 0  # 8
    history_xl = 0  # 5

    hostname = 'localhost'
    username = 'predictuser'
    password = 'password'
    database = 'predictatron'
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cur = conn.cursor()
    date_list_sql = "SELECT snapshot_date FROM snapshot ORDER BY snapshot_date"
    date_list = []
    cur.execute(date_list_sql)
    for snapshot_date_item in cur.fetchall():
        date_list.append(snapshot_date_item[0].strftime("%Y-%m-%d"))

    the_sql = "SELECT id, snapshot_date, snapshot_name, backlog_small, backlog_medium, backlog_large, backlog_xl, history_weeks, history_small, history_medium, history_large, history_xl FROM snapshot where snapshot_date = '" + snapshotdate + "'::date"
    cur.execute(the_sql)

    for id_x, snapshot_date_x, snapshot_name_x, backlog_small_x, backlog_medium_x, backlog_large_x, backlog_xl_x, history_weeks_x, history_small_x, history_medium_x, history_large_x, history_xl_x in cur.fetchall():
        snapshot_date = snapshot_date_x
        snapshot_name = snapshot_name_x
        backlog_small = backlog_small_x
        backlog_medium = backlog_medium_x
        backlog_large = backlog_large_x
        backlog_xl = backlog_xl_x
        history_weeks = history_weeks_x
        history_small = history_small_x
        history_medium = history_medium_x
        history_large = history_large_x
        history_xl = history_xl_x
    conn.close()

    # print(snapshot_date, file=sys.stderr)

    # multiplier = 1.5  # safety margin multiplier
    min_multiplier = 0.7
    max_multiplier = 2.0
    backlog = (backlog_small*5) + (backlog_medium * 8) + (backlog_large * 13) + (backlog_xl * 21)
    velocity = round(((history_small*5)+(history_medium*8)+(history_large*13+(history_xl*21)))/history_weeks, 2)
    med = int((backlog/velocity)*float(multiplier))
    min_val = int(med * min_multiplier)
    max_val = int(med * max_multiplier)
    magnifier = 850/max_val
    p1_epics_total = calculate_period_1_epics()
    return render_template("dashboard.html",
                           backlog=backlog, velocity=velocity, multiplier=multiplier, min=min_val, med=med,
                           max=max_val, magnifier=magnifier, snapshot_date=snapshot_date, snapshot_name=snapshot_name,
                           history_weeks=history_weeks, p1_epics_total=p1_epics_total, date_list=date_list)


@app.route('/epics')
def epics():
    epics = {}
    hostname = 'localhost'
    username = 'predictuser'
    password = 'password'
    database = 'predictatron'
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cur = conn.cursor()
    cur.execute("SELECT epic_id, snapshot_date, goal_period, epic_title, status, kanban_small, kanban_medium, kanban_large, kanban_xl FROM epic")
    for epic_id_x, snapshot_date_x, goal_period_x, epic_title_x, status_x, kanban_small_x, kanban_medium_x, kanban_large_x, kanban_xl_x in cur.fetchall():
        epics[epic_id_x] = {'snapshot_date': snapshot_date_x, 'goal_period': goal_period_x, 'epic_title': epic_title_x,
                            'status': status_x, 'kanban_small': kanban_small_x, 'kanban_medium': kanban_medium_x,
                            'kanban_large': kanban_large_x, 'kanban_xl': kanban_xl_x}
    conn.close()
    print(str(epics))
    return render_template("epics.html", epics=epics)


@app.route('/info')
def info():
    return platform.python_version()

@app.route('/dbtest')
def dbtest():
    hostname = 'localhost'
    username = 'predictuser'
    password = 'password'
    database = 'predictatron'
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cur = conn.cursor()
    cur.execute("SELECT id, snapshot_date, backlog_small, backlog_medium, backlog_large, backlog_xl, history_weeks, history_small, history_medium, history_large, history_xl FROM snapshot")
    return_value = ''
    for id_x, snapshot_date, backlog_small, backlog_medium, backlog_large, backlog_xl, history_weeks, history_small, history_medium, history_large, history_xl in cur.fetchall():
        return_value += str(id_x) + ' ' + str(snapshot_date) + extra_stuff() + '<br/>'
    conn.close()
    return return_value


@app.route('/login/<user>')
def index(user=None):
    return render_template("user.html", user=user)


@app.route('/request/method')
def request_method():
    return "Method used: %s" % request.method


@app.route('/bingo', methods=['GET', 'POST'])
def bingo():
    if request.method == 'POST':
        return "You are using POST"
    else:
        return "You are probably using GET"


@app.route('/hello/<person>')
def hello(person):
    return "<h3>Hello %s</h3>" % person


@app.route('/profile/<person>')
def profile(person):
    return render_template("profile.html", person=person)


@app.route('/post/<int:post_id>')
def post(post_id):
    return "Blog post %s" % post_id

if __name__ == '__main__':
    app.run(debug=True)
