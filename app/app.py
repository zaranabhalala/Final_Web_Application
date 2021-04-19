from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

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
    user = {'username': 'Name Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, Names=result)

@app.route('/view/<string:Name>', methods=['GET'])
def record_view(Name):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE Name =%s', Name)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', Player=result[0])

@app.route('/edit/<string:Name>', methods=['GET'])
def form_edit_get(Name):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlb_players WHERE Name=%s', Name)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', Player=result[0])

@app.route('/edit/<string:Name>', methods=['POST'])
def form_update_post(Name):
    cursor = mysql.get_db().cursor()
    inputData = (str(request.form.get('Name')), str(request.form.get('Team')), str(request.form.get('Position')),
                 str(request.form.get('Height_inches')), str(request.form.get('Weight_lbs')),
                 str(request.form.get('Age')), Name)
    sql_update_query = """UPDATE mlb_players t SET t.Name = %s, t.Team = %s, t.Position = %s, t.Height_inches = 
    %s, t.Weight_lbs = %s, t.Age = %s WHERE t.Name = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/names/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Player Form')

@app.route('/Names/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Team'), request.form.get('Position'),
                 request.form.get('Height_inches'), request.form.get('Weight_lbs'),
                 request.form.get('Age'),)
    sql_insert_query = """INSERT INTO mlb_players (Name,Team,Position,Height_inches,Weight_lbs,Age) 
    VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)