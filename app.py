# sqlite3を使えるようにする
import sqlite3

from flask import Flask,render_template,request,redirect,session
# flaskのflask,render_template,sessionを使用します宣言
app= Flask(__name__)

# sessionを使うときに書く 鍵
app.secret_key ="usakuma"

@app.route("/")
def top():
    return redirect("/login")

@app.route("/test")
def test():
    name = "flask"
    return render_template("test.html",name = name)

@app.route("/greet/<text>")
def hello(text):
    name = "flask"
    return text + "さん、こんにちは"

@app.route("/test2")
def test2():
    name = "flask"
    return render_template("test2.html",name = name)

# 404ページを表示
@app.errorhandler(404)
def notfound(code):
    return "ここは404ページです"



# 2日目データベースの接続
@app.route("/dbtest")
def dbtest():
    # データベースに接続
    conn = sqlite3.connect('flask.db')
    
    # どこのデータを抜くかカーソルを充てる。カーソル→矢印
    c = conn.cursor()
    
    # execute:実行する
    c.execute("select name, adress from users where id = 2")
    
    # fetchone:フェッチ：実際に取得する
    user_info = c.fetchone()
    
    # データベース接続終了
    c.close()
    
    # user_infoの中身を確認
    print(user_info)
    return render_template("dbtest.html",user_info = user_info)



# データベースを追加
@app.route("/add")
def add():
    return render_template("add.html")

# データを追加するボタンの処理
@app.route("/add",methods=["POST"])
def add_post():
    if "user_id" in session:
        # add.htmlからformのname="task"を取得
        task = request.form.get("task")
        # データベースに接続
        conn = sqlite3.connect("flask.db")
        c = conn.cursor()
        # (task,)のカンマは忘れずに！タプル型なので！
        # ?に(task,)が入るよ
        # insert into はデータを追加
        c.execute("insert into task values(null ,?)", (task,))
        conn.commit()
        c.close()
        return "データを追加できました！"
    else:
        return redirect("/login")



@app.route("/task_list")
def task_list():
    if "user_id" in session:
        conn = sqlite3.connect("flask.db")
        c = conn.cursor()
        c.execute("select id,task from task ")
        task_list = []
        for row in c.fetchall():
            task_list.append({"id":row[0],"task":row[1]})
        c.close()
        return render_template("task_list.html", task_list = task_list)
    else:
        return redirect("/login")

@app.route("/del/<int:id>")
def del_task(id):
    if "user_id" in session:
        conn = sqlite3.connect("flask.db")
        c = conn.cursor()
        c.execute("delete from task where id = ?",(id,))
        conn.commit()
        conn.close()
        return redirect("/task_list")
    # データベースに変更があるときはcommit()を書くよ
    # import追加するのを忘れないように redirect
    else:
        return redirect("/login")

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" in session:
        conn = sqlite3.connect("flask.db")
        c = conn.cursor()
        c.execute("select task from task where id = ?",(id,))
        task = c.fetchone()
        conn.close()
        task = task[0]
        item = {"id":id,"task":task}
        print(task)
        return render_template("edit.html",task = item)
    else:
        return redirect("/login")

@app.route("/edit" , methods =["POST"])
def update_task():
    if "user_id" in session:
        item_id = request.form.get("task_id")
        item_id = int(item_id)
        task = request.form.get("task")
        conn = sqlite3.connect("flask.db")
        c = conn.cursor()
        c.execute("update task set task = ? where id = ?",(task ,item_id))
        conn.commit()
        conn.close()
        return redirect("/task_list")
    else:
        return redirect("/login")

# 登録画面
@app.route("/regist",methods =["GET"])
def regist_get():
    return render_template("regist.html")

@app.route("/regist",methods =["POST"])
def regist_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect("flask.db")
    c = conn.cursor()
    c.execute("insert into user values(null,?,?)",(name,password))
    user_password = c.fetchone()
    conn.commit()
    conn.close()
    return redirect("/login")


# ログイン
@app.route("/login",methods= ["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login" , methods =["POST"])
def login_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect("flask.db")
    c = conn.cursor()
    c.execute("select id from user where name =? and password =?",(name,password))
    user_id = c.fetchone()
    conn.close()
    if user_id == None:
        return render_template("login.html")
    else:
        session["user_id"] = user_id[0]
        return redirect("/task_list")

# 一番下に書くよ
if __name__ == "__main__":
    # サーバーを起動するよ
    app.run(debug=True, host ="0.0.0.0",port=8888)
    # デバックモードを有効にするよ