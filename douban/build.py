"""
该模块主要用于管理电影相关数据，包括数据库的重置、电影数据模型的定义，
以及从 CSV 文件导入数据、数据的增删改查等操作。
"""
import os
import csv
from peewee import SqliteDatabase, Model, CharField, FloatField, TextField, IntegerField

# ===== 1. 删除旧数据库，避免表结构不一致 =====
def reset_db(db_path="movie.db"):
    """
    删除指定路径的数据库文件（如果存在）。

    Args:
        db_path (str): 数据库文件路径，默认为 "movie.db"。
    """
    if os.path.exists(db_path):
        os.remove(db_path)

# ===== 2. 初始化数据库连接 =====
db = SqliteDatabase("movie.db")

# ===== 3. 定义数据模型 =====
class Movie(Model):
    """
    电影数据模型类，用于表示电影相关信息。

    Attributes:
        title (CharField): 电影标题，最大长度为 100。
        rating_num (FloatField): 电影评分。
        comment_num (TextField): 电影评论数量。
        year (IntegerField): 电影上映年份，可为空。
    """
    title = CharField(max_length=100)
    rating_num = FloatField()
    comment_num = TextField()
    year = IntegerField(null=True)

    class Meta:
        database = db
        table_name = 'douban_movie'

# ===== 4. 从 CSV 导入数据到数据库 =====
def save_data_from_csv(csv_path):
    """
    从指定的 CSV 文件中读取电影数据，并导入到数据库中。

    Args:
        csv_path (str): CSV 文件路径。
    """
    # 假设数据库已连接
    db.create_tables([Movie], safe=True)

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                title = row['标题']
                rating_num = float(row['评分']) if row['评分'] else 0.0
                comment_num = row.get('评论数', '')
                year_str = row.get('年份', '')
                year = int(year_str) if year_str.isdigit() else None
                Movie.create(title=title, rating_num=rating_num, comment_num=comment_num, year=year)
            except ValueError as e:
                print(f"⚠️ 跳过一条记录: 数据转换错误 - {e}")
            except KeyError as e:
                print(f"⚠️ 跳过一条记录: 缺少列 - {e}")

    print("✅ 数据导入完成")

# ===== 5. 插入单条数据 =====
def insert_single(title, rating_num, comment_num, year):
    """
    向数据库中插入单条电影数据。

    Args:
        title (str): 电影标题。
        rating_num (float): 电影评分。
        comment_num (str): 电影评论数量。
        year (int): 电影上映年份。
    """
    # 假设数据库已连接
    Movie.create(title=title, rating_num=rating_num, comment_num=comment_num, year=year)
    print(f"✅ 插入电影: {title}")

# ===== 6. 批量插入数据 =====
def insert_batch(data_list):
    """
    批量插入电影数据到数据库中。

    Args:
        data_list (list): 包含电影数据字典的列表，每个字典应包含 'title', 'rating_num', 'comment_num', 'year' 键值对。
    """
    # 假设数据库已连接
    Movie.insert_many(data_list).execute()
    print(f"✅ 批量插入 {len(data_list)} 条电影数据")

# ===== 7. 查询所有记录 =====
def query_all():
    """
    查询数据库中所有的电影记录，并打印电影标题、评分和年份。
    """
    print("📋 所有电影：")
    for movie in Movie.select():
        print(movie.title, movie.rating_num, movie.year)

# ===== 8. 查询指定年份的电影 =====
def query_by_year(year):
    """
    查询指定年份上映的电影记录，并打印电影标题和评分。

    Args:
        year (int): 要查询的电影上映年份。
    """
    print(f"\n🎬 {year}年电影：")
    for movie in Movie.select().where(Movie.year == year):
        print(movie.title, movie.rating_num)

# ===== 9. 查询包含指定关键词的电影 =====
def query_by_title_keyword(keyword):
    """
    查询标题中包含指定关键词的电影记录，并打印电影标题和评分。

    Args:
        keyword (str): 要搜索的关键词。
    """
    print(f"\n🔍 标题包含“{keyword}”的电影：")
    for movie in Movie.select().where(Movie.title.contains(keyword)):
        print(movie.title, movie.rating_num)

# ===== 10. 更新指定电影的评分 =====
def update_rating(title, new_rating):
    """
    更新指定电影的评分。

    Args:
        title (str): 要更新评分的电影标题。
        new_rating (float): 新的电影评分。
    """
    updated = Movie.update(rating_num=new_rating).where(Movie.title == title).execute()
    if updated:
        print(f"\n✅ 已更新《{title}》评分为 {new_rating}")
    else:
        print(f"\n⚠️ 未找到电影《{title}》进行更新")

# ===== 11. 删除指定电影 =====
def delete_movie(title):
    """
    从数据库中删除指定标题的电影记录。

    Args:
        title (str): 要删除的电影标题。
    """
    deleted = Movie.delete().where(Movie.title == title).execute()
    if deleted:
        print(f"🗑️ 已删除《{title}》")
    else:
        print(f"⚠️ 未找到电影《{title}》进行删除")

# ===== 12. 统计指定年份电影数量 =====
def count_by_year(year):
    """
    统计指定年份上映的电影数量。

    Args:
        year (int): 要统计电影数量的年份。

    Returns:
        int: 指定年份上映的电影数量。
    """
    count = Movie.select().where(Movie.year == year).count()
    print(f"📊 {year}年上映的电影数量：{count}")
    return count

# ===== 13. 分页查询电影，每页 page_size 条 =====
def paginate_movies(page=1, page_size=25):
    """
    分页查询电影记录。

    Args:
        page (int): 要查询的页码，默认为 1。
        page_size (int): 每页显示的电影数量，默认为 25。
    """
    print(f"\n📄 第 {page} 页电影（每页{page_size}条）：")
    query = Movie.select().paginate(page, page_size)
    for movie in query:
        print(movie.title)

# ===== 14. 主程序入口示范 =====
if __name__ == "__main__":
    CSV_PATH = r"C:\Users\20342\Desktop\final\CSV\douban_movies.csv"

    reset_db()
    db.connect()
    try:
        save_data_from_csv(CSV_PATH)

        insert_single(title="魂断蓝桥", rating_num=8.7, comment_num="10万人评论", year=1940)

        batch_data = [
            {"title": "冰雪奇缘", "rating_num": 7.9, "comment_num": "12万人评论", "year": 2013},
            {"title": "蜘蛛侠：纵横宇宙", "rating_num": 8.8, "comment_num": "20万人评论", "year": 2023},
            {"title": "流浪地球2", "rating_num": 8.3, "comment_num": "25万人评论", "year": 2023},
        ]
        insert_batch(batch_data)

        query_all()
        query_by_year(2023)
        query_by_title_keyword("蜘蛛侠")
        update_rating("魂断蓝桥", 9.0)
        delete_movie("冰雪奇缘")
        count_by_year(2010)
        paginate_movies(page=1, page_size=25)

    finally:
        db.close()

