# sqlite3を使えるようにする
import sqlite3

from flask import Flask,render_template,request
# flaskのflask,render_templateを使用します宣言
app= Flask(__name__)


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



@app.route("/list")
def task_list():
    conn = sqlite3.connect("flask.db")
    c = conn.cursor()
    c.execute("select id,task from task ")
    task_list = []
    for row in c.fetchall():
        task_list.append({"id":row[0],"task":row[1]})
    c.close()
    return render_template("list.html", task_list = task_list)




# 一番下に書くよ
if __name__ == "__main__":
    # サーバーを起動するよ
    app.run(debug=True)
    # デバックモードを有効にするよ