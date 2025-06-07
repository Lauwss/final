"""
这是一个基于 Flask 的简单登录应用模块。
该模块定义了应用的路由和处理函数，包括主页、登录表单展示和登录验证功能。
"""

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    处理主页的请求。
    返回渲染后的 home.html 模板。
    """
    print("✅ 渲染 home.html")
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    """
    处理登录表单页面的 GET 请求。
    返回渲染后的 form.html 模板，用于展示登录表单。
    """
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    """
    处理登录表单的 POST 请求。
    从请求中获取用户名和密码，进行验证。
    如果用户名和密码正确，返回渲染后的 signin-ok.html 模板；否则返回错误提示。
    """
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if username == 'root' and password == '0416':
        return render_template('signin-ok.html', username=username)
    return '<h3>用户名或密码错误</h3><p><a href="/signin">返回登录</a></p>'

if __name__ == '__main__':
    app.run(debug=True)