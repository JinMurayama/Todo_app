from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime
import time
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
config={'user':'', 'password':'', 'host':'', 'db':''};
conn = mysql.connector.connect(**config)
cur = conn.cursor(buffered=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/regist')
def regist():
    return render_template("regist.html")
    
@app.route("/confirm", methods=['POST', 'GET'])
def confirm():
    if request.method == 'POST':
        if request.form["new_password"] == request.form["again_password"] and request.form["new_password"] != "":
            name = request.form["new_user_name"]
            password=request.form["new_password"]
            cur.execute("INSERT INTO `user` (`username`, `password`) VALUES ('{name}','{password}');".format(name=name, password=password))
            conn.commit()   
            return render_template("regist_thanks.html")
        if request.form["new_user_name"] == "":
            flash("ユーザー名を入力してください。", "failed")
        if request.form["new_password"] == "":
            flash("パスワードを入力してください。", "failed")
        if request.form["new_password"] != request.form["again_password"]:
            flash("パスワードが異なります", "failed")
        return render_template("regist.html")
                
@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/regist_thanks")
def regist_thanks():
    return render_template("index.html")
    
@app.route('/list', methods=['POST', 'GET'])
def display():
    if request.method== 'POST':
        name = request.form['user_name']
        password=request.form['password']
        cur.execute("SELECT 1 from user WHERE username = '" + name + "' AND password = '" + password + "'")
        result=cur.fetchall()
        if not result:
            flash("ユーザー名が異なります", "failed")
            flash("パスワードが異なります", "failed")
            return render_template('index.html')
        else:
            session["name"] = name
            tasks = pick()
            return render_template('list.html', name=name, tasks=tasks)
    else:
        name=session.get('name')
        cur.execute("SELECT * from task WHERE username = '"+ name + "'")
        cur.fetchall()
        tasks = pick()
        return render_template("list.html", name=name, tasks=tasks)
        
@app.route('/add', methods=['POST','GET'])
def add():
    if request.method=='POST':
        username=session.get("name")
        tstr = request.form["deadline"]
        sql = (request.form['title'], request.form['contents'], tstr, request.form["status"], username)
        cur.execute("INSERT INTO task (title, contents, deadline, status, username) VALUES (%s, %s, %s, %s, %s)", sql)
        conn.commit()
        tasks=pick()
        return render_template("list.html", name = username,tasks=tasks)
    else:
        return render_template("add.html")

@app.route('/delete', methods=["POST"])
def delete():
    id = request.form["no"]
    session["no"]=id
    cur.execute("delete from task where id = '" + id + "'")
    conn.commit()
    tasks = pick()
    return render_template('list.html', name=session.get('name'), tasks=tasks)

@app.route('/edit', methods=['POST'])
def edit():
    session["no"] = request.form["no"]
    cur.execute("select * from task where id = '" + session.get("no") + "'")
    tasks=cur.fetchall()
    return render_template("edit.html", tasks=tasks)

@app.route('/edit_register', methods=["POST"])
def edit_register():
    tstr = request.form["deadline"]
    sql = (request.form['title'], request.form['contents'], tstr, request.form["status"], session.get("no"))
    cur.execute('UPDATE task SET title = %s, contents= %s, deadline= %s, status=%s WHERE id = %s', sql)
    conn.commit()
    name=session.get('name')
    tasks = pick()
    return render_template("list.html", name=name, tasks=tasks)
    
def pick():
    username = session.get('name')
    cur.execute("SELECT * FROM task WHERE username= '" + username + "'")
    tasks = cur.fetchall()
    return tasks

app.secret_key = ''

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
