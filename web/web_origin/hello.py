from flask import Flask, request, render_template
from flasgger import Swagger
import json
import os

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    主页
    ---
    get:
      description: 返回主页
      responses:
        200:
          description: 返回 home.html 页面
    post:
      description: 主页 POST 请求（通常不处理）
      responses:
        200:
          description: 返回 home.html 页面
    """
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    """
    登录表单页面
    ---
    get:
      description: 返回登录表单页面
      responses:
        200:
          description: 返回 form.html 页面
    """
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    """
    登录操作
    ---
    post:
      description: 验证用户名和密码
      parameters:
        - name: username
          in: formData
          type: string
          required: true
          description: 用户名
        - name: password
          in: formData
          type: string
          required: true
          description: 密码
      responses:
        200:
          description: 登录成功或失败页面
    """
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if username == 'root' and password == '0416':
        return render_template('signin-ok.html', username=username)
    return '<h3>用户名或密码错误</h3><p><a href="/signin">返回登录</a></p>'

if __name__ == '__main__':
    # 👇 获取当前 Python 文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    swagger_path = os.path.join(current_dir, 'swagger.json')

    # 👇 请求 Swagger 文档并保存为 JSON
    with app.test_client() as client:
        response = client.get('/apispec_1.json')
        if response.status_code == 200:
            with open(swagger_path, 'w', encoding='utf-8') as f:
                json.dump(response.json, f, ensure_ascii=False, indent=2)
            print(f"✅ Swagger API 文档已保存为：{swagger_path}")
        else:
            print("⚠️ 无法获取 Swagger 文档")

    app.run(debug=True)
