from flask import Flask,render_template
# flaskのflask,render_templateを使用します宣言
app= Flask(__name__)

@app.route("/test")
def test():
    return render_template("test.html")









if __name__ == "__main__":
    # サーバーを起動するよ
    app.run(debug=True)
    # デバックモードを有効にするよ