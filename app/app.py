from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from utilities import sendemail
import sys

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

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html', title='SignUp Page')

@app.route('/index', methods=['GET'])
def show_index():
    user = {'username': 'Zarana and Jay'}
    sendemail.sendemail('zvb2@njit.edu')
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPlayersImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, Players=result)

@app.route('/logins/new', methods=['POST'])
def add_login():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('userName'), request.form.get('userEmail'), request.form.get('userPassword'),
                 request.form.get('userHash'))
    sql_insert_query = """INSERT INTO tblTempUsers (userName,userEmail,userPassword,userHash) 
    VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/checklogin', methods=['POST'])
def form_check_login():
    strEmail = str(request.form.get('email'))
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblUsers WHERE userEmail=%s', strEmail)
    row_count = cursor.rowcount
    if row_count == 0:
        print('No rows returned', file=sys.stderr)
        return render_template('signup.html', title='Signup')
    else:
        result = cursor.fetchall()

        if str(result[0]['userPassword']) == str(request.form.get('pswd')):

            user = {'username': str(result[0]['userName'])}
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM tblPlayersImport')
            result = cursor.fetchall()
            return render_template('index.html', title='Home', user=user, players=result)

        else:
            print('In Else', file=sys.stderr)
            return render_template('login.html', title='Login Page')

@app.route('/view/<int:player_id>', methods=['GET'])
def record_view(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id =%s', player_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', Player=result[0])


@app.route('/edit/<int:player_id>', methods=['GET'])
def form_edit_get(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE id =%s', player_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', Player=result[0])


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