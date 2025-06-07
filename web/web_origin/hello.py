from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
     print("✅ 渲染 home.html")
     return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if username == 'root' and password == '0416':
        return render_template('signin-ok.html', username=username)
    else:
        return '<h3>用户名或密码错误</h3><p><a href="/signin">返回登录</a></p>'

if __name__ == '__main__':
    app.run(debug=True)
