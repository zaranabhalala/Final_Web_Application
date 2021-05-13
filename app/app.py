from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from utilities import sendemail
import sys
from datetime import datetime
import random

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'mlbPlayers'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html', title='Login Page')

@app.route('/statistics', methods=['GET'])
def charts_view():
    legend = 'Player Count in Each Position'
    labels = []
    cursor = mysql.get_db().cursor()
    cursor.execute(
        'SELECT position FROM mlb_players GROUP BY position')
    for temp in cursor.fetchall():
        labels.append(list(temp.values())[0])
    values = []
    cursor.execute('SELECT COUNT(*) FROM mlb_players GROUP BY position ')
    for temp in cursor.fetchall():
        values.append(list(temp.values())[0])
    result = cursor.fetchall()
    return render_template('flowchart.html', title='Home', player=result, player_labels=labels,
                           player_legend=legend,
                           player_values=values)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', title='Login Page')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html', title='SignUp Page')

@app.route('/index', methods=['GET'])
def show_index():
    user = {'username': 'Zarana and Jay'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, players=result)

@app.route('/logins/new', methods=['POST'])
def add_login():
    cursor = mysql.get_db().cursor()
    strEmail = str(request.form.get('email'))

    cursor.execute('SELECT * FROM tblUsers WHERE userEmail=%s', strEmail)

    row_count = cursor.rowcount
    if row_count == 0:
        strPassword = request.form.get('pswd')
        strName = request.form.get('name')
        print('No rows returned', file=sys.stderr)
        random.seed(datetime.now())
        strHash = str(random.randint(123234, 1232315324))
        inputData = (strName, strEmail, strPassword, strHash)
        sql_insert_query = """INSERT INTO tblUsers (userName,userEmail,userPassword,userHash) 
                VALUES (%s, %s,%s, %s) """
        cursor.execute(sql_insert_query, inputData)
        mysql.get_db().commit()
        sendemail.sendemail(strEmail, strHash)
        return render_template('login.html', title='Login Page')
    else:
        print('Login already exists', file=sys.stderr)
        cursor.execute('SELECT * FROM tblErrors where errName=%s', 'USER_EXISTS')
        result = cursor.fetchall()
        return render_template('notify.html', title='Notify', player=result[0])

@app.route('/checklogin', methods=['POST'])
def form_check_login():
    strEmail = str(request.form.get('email'))
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblUsers WHERE userEmail=%s', strEmail)
    row_count = cursor.rowcount
    if row_count == 0:
        print('No rows returned', file=sys.stderr)
        cursor.execute('SELECT * FROM tblErrors where errName=%s', 'USER_NOT_FOUND')
        result = cursor.fetchall()
        return render_template('notify.html', title='Notify', player=result[0])
    else:
        result = cursor.fetchall()

        if result[0]['userHash'] != '':
            print('userHash ' + result[0]['userHash'], file=sys.stderr)
            cursor.execute('SELECT * FROM tblErrors where errName=%s', 'EMAIL_NOT_VERIFIED')
            result = cursor.fetchall()
            return render_template('notify.html', title='Notify', player=result[0])

        if str(result[0]['userPassword']) == str(request.form.get('pswd')):

            user = {'username': str(result[0]['userName'])}
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM mlb_players')
            result = cursor.fetchall()
            return render_template('index.html', title='Home', user=user, players=result)

        else:
            print('Invalid Id/PWD', file=sys.stderr)
            cursor.execute('SELECT * FROM tblErrors where errName=%s', 'INVALID_LOGIN')
            result = cursor.fetchall()
            return render_template('notify.html', title='Notify', player=result[0])

@app.route('/validateLogin/<int:intHash>', methods=['GET', 'POST'])
def validateLogin(intHash):
        cursor = mysql.get_db().cursor()
        inputData = str(intHash)
        sql_update_query = """UPDATE tblUsers t SET t.userHash = '' WHERE t.userHash = %s """
        cursor.execute(sql_update_query, inputData)
        mysql.get_db().commit()
        cursor.execute('SELECT * FROM tblErrors where errName=%s', 'EMAIL_VERIFIED')
        result = cursor.fetchall()
        return render_template('notify.html', title='Notify', player=result[0])

@app.route('/view/<int:player_id>', methods=['GET'])
def record_view(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id =%s', player_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['GET'])
def form_edit_get(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id =%s', player_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['POST'])
def form_update_post(player_id):
    cursor = mysql.get_db().cursor()
    inputData = (str(request.form.get('Name')), str(request.form.get('Team')), str(request.form.get('Position')),
                 str(request.form.get('Height_inches')), str(request.form.get('Weight_lbs')),
                 str(request.form.get('Age')), player_id)
    sql_update_query = """UPDATE mlb_players t SET t.Name = %s, t.Team = %s, t.Position = %s, t.Height_inches = 
    %s, t.Weight_lbs = %s, t.Age = %s WHERE t.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/Names/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Player Form')


@app.route('/Names/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Team'), request.form.get('Position'),
                 request.form.get('Height_inches'), request.form.get('Weight_lbs'),
                 request.form.get('Age'))
    sql_insert_query = """INSERT INTO mlb_players (Name,Team,Position,Height_inches,Weight_lbs,Age) 
    VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:player_id>', methods=['POST'])
def form_delete_post(player_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlb_players WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/Names', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/Names/<int:player_id>', methods=['GET'])
def api_retrieve(player_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id =%s', player_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/Names/<int:player_id>', methods=['PUT'])
def api_edit(player_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Name'], content['Team'], content['Position'],
                 content['Height_inches'], content['Weight_lbs'],
                 content['Age'], player_id)
    sql_update_query = """UPDATE mlb_players t SET t.Name = %s, t.Team = %s, t.Position = %s, t.Height_inches = 
            %s, t.Weight_lbs = %s, t.Age = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/Names/', methods=['POST'])
def api_add() -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Name'], content['Team'], content['Position'],
                 content['Height_inches'], content['Weight_lbs'],
                 content['Age'])
    sql_insert_query = """INSERT INTO mlb_players (Name,Team,Position,Height_inches,Weight_lbs,Age) 
        VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/Names/<int:player_id>', methods=['DELETE'])
def api_delete(player_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlb_players WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
