from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_movies():
    movies = []
    with open(r'C:\Users\20342\Desktop\final\CSV\douban_movies.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append(row)
    return movies

@app.route('/', methods=['GET', 'POST'])
def index():
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
