from flask import Flask,render_template
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










if __name__ == "__main__":
    # サーバーを起動するよ
    app.run(debug=True)
    # デバックモードを有効にするよ