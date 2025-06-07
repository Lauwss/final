"""
该模块使用 Flask 框架创建一个简单的 Web 应用，用于根据用户输入的年份筛选电影数据。
用户可以在网页上输入年份，应用将显示该年份上映的电影标题。
"""
import csv
from flask import Flask, render_template, request

app = Flask(__name__)

def load_movies():
    """
    从指定的 CSV 文件中加载电影数据。

    Returns:
        list: 包含电影数据的字典列表，每个字典表示一部电影的信息。
    """
    movies = []
    csv_file_path = (
        r'C:\Users\20342\Desktop\final\CSV'
        r'\douban_movies.csv'
    )
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append(row)
    return movies

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    处理根路径的请求，根据用户输入的年份筛选电影数据并渲染模板。

    如果是 POST 请求，且用户输入的年份是有效的数字，
    则筛选出该年份上映的电影标题。

    Returns:
        str: 渲染后的 HTML 页面。
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
    app.run(debug=True)