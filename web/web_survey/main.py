"""
该模块使用 Flask 框架创建一个简单的 Web 应用，用于根据用户输入的年份筛选电影数据。
用户可以在网页上输入年份，应用将显示该年份上映的电影标题。
"""

import csv
import os
import json
from flask import Flask, render_template, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

def load_movies():
    """
    从指定的 CSV 文件中加载电影数据。

    Returns:
        list: 包含电影数据的字典列表，每个字典表示一部电影的信息。
    """
    movies = []
    csv_file_path = (
        r'C:\Users\20342\Desktop\final\CSV\douban_movies.csv'
    )
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append(row)
    return movies

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    主页 - 根据年份筛选电影
    ---
    get:
      description: 显示首页，等待用户输入年份
      responses:
        200:
          description: 返回 index.html 页面
    post:
      description: 根据用户输入的年份筛选电影并展示
      parameters:
        - name: release_year
          in: formData
          type: string
          required: true
          description: 用户输入的年份
      responses:
        200:
          description: 返回筛选后的电影列表页面
    """
    movies = load_movies()
    filtered_movies = []
    year_input = ''

    if request.method == 'POST':
        year_input = request.form.get('release_year', '').strip()
        if year_input.isdigit():
            filtered_movies = [m['\ufeff标题'] for m in movies if m['年份'] == year_input]

    return render_template('index.html', movies=filtered_movies, year=year_input)

if __name__ == '__main__':
    # 保存 Swagger 文档到当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    swagger_path = os.path.join(current_dir, 'swagger.json')

    with app.test_client() as client:
        response = client.get('/apispec_1.json')
        if response.status_code == 200:
            with open(swagger_path, 'w', encoding='utf-8') as f:
                json.dump(response.json, f, ensure_ascii=False, indent=2)
            print(f"✅ Swagger API 文档已保存为：{swagger_path}")
        else:
            print("⚠️ 无法获取 Swagger 文档")

    app.run(debug=True)
