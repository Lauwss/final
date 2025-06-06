from peewee import *
import pymysql
from datetime import datetime
import csv

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '0416',
    'charset': 'utf8mb4'
}

# 创建数据库（如果不存在）
def create_database_if_not_exists(db_name):
    mysql_server = MySQLDatabase(None)
    mysql_server.init(database='mysql', **DB_CONFIG)
    try:
        mysql_server.connect()
        mysql_server.execute_sql(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"数据库 '{db_name}' 已创建/存在")
    except Exception as e:
        print(f"创建数据库失败: {e}")
    finally:
        mysql_server.close()

# 配置数据库连接
db = MySQLDatabase('test_db', **DB_CONFIG)

# 定义模型
class BaseModel(Model):
    class Meta:
        database = db

class Movie(BaseModel):
    title = CharField(max_length=100, unique=True)
    rating = FloatField(default=0.0)
    comment_count = IntegerField(default=0)
    release_date = DateField(null=True)

    class Meta:
        table_name = 'movies'

# 插入单条数据
def insert_single_movie(title, rating, comment_count=0, release_date=None):
    try:
        with db.atomic():
            if isinstance(release_date, str):
                release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
            movie = Movie.create(
                title=title,
                rating=rating,
                comment_count=comment_count,
                release_date=release_date
            )
            print(f"插入成功：{movie.title}")
            return movie
    except IntegrityError:
        print(f"错误：电影 '{title}' 已存在")
        return None

# 批量插入数据（列表形式）
def batch_insert_movies(movie_list):
    try:
        with db.atomic():
            for movie_data in movie_list:
                if isinstance(movie_data.get('release_date'), str):
                    movie_data['release_date'] = datetime.strptime(
                        movie_data['release_date'], "%Y-%m-%d"
                    ).date()
            Movie.insert_many(movie_list).execute()
            print(f"批量插入成功：共 {len(movie_list)} 条")
    except IntegrityError as e:
        print(f"批量插入失败：{e}")

# 从 CSV 文件导入数据到数据库
def import_csv_to_database(csv_file_path):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            movie_data_list = []

            for row in reader:
                release_date = row.get('release_date')
                if release_date:
                    row['release_date'] = datetime.strptime(release_date, "%Y-%m-%d").date()
                row['rating'] = float(row['rating'])
                row['comment_count'] = int(row['comment_count'])
                movie_data_list.append(row)

            with db.atomic():
                Movie.insert_many(movie_data_list).execute()
                print(f"成功导入 {len(movie_data_list)} 条数据")

    except FileNotFoundError:
        print(f"错误：文件 {csv_file_path} 不存在")
    except Exception as e:
        print(f"导入失败：{e}")
        db.rollback()

# 查询所有记录
def query_all_movies():
    return Movie.select()

# 查询指定年份上映的电影
def query_movies_by_year(year=2023):
    return Movie.select().where(
        Movie.release_date.year == year
    ).order_by(Movie.release_date.desc())

# 查询指定电影
def query_movie_by_title(title):
    try:
        return Movie.get(Movie.title == title)
    except Movie.DoesNotExist:
        print(f"错误：未找到电影 '{title}'")
        return None

# 更新电影评分
def update_movie_rating(title, new_rating):
    try:
        movie = Movie.get(Movie.title == title)
        movie.rating = new_rating
        movie.save()
        print(f"更新成功：{movie.title} 评分变为 {new_rating}")
        return movie
    except Movie.DoesNotExist:
        print(f"错误：未找到电影 '{title}'")
        return None

# 删除指定电影
def delete_movie_by_title(title):
    try:
        count = Movie.delete().where(Movie.title == title).execute()
        if count > 0:
            print(f"删除成功：已删除 {count} 条 '{title}' 记录")
            return True
        else:
            print(f"错误：未找到电影 '{title}'")
            return False
    except Exception as e:
        print(f"删除失败：{e}")
        return False

# 统计指定年份出品的电影数量
def count_movies_by_year(year=2010):
    return Movie.select().where(
        Movie.release_date.year == year
    ).count()

# 分页查询
def paginate_movies(page=1, page_size=25):
    start = (page - 1) * page_size
    return Movie.select().order_by(Movie.release_date.desc()).paginate(page, page_size)

# 从数据库导出数据到 CSV 文件
def export_database_to_csv(csv_file_path):
    try:
        movies = query_all_movies()
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'rating', 'comment_count', 'release_date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for movie in movies:
                movie_data = {
                    'title': movie.title,
                    'rating': movie.rating,
                    'comment_count': movie.comment_count,
                    'release_date': movie.release_date.strftime("%Y-%m-%d") if movie.release_date else None
                }
                writer.writerow(movie_data)
        print(f"成功导出数据到 {csv_file_path}")
    except Exception as e:
        print(f"导出失败：{e}")

if __name__ == "__main__":
    # 初始化数据库
    create_database_if_not_exists('test_db')
    db.connect()
    db.create_tables([Movie])
    print("数据库初始化完成")

    # 导入 CSV 数据
    csv_file_path = 'C:/Users/20342/Desktop/final/CSV/douban_movies.csv'
    import_csv_to_database(csv_file_path)

    # 插入单条数据示例
    insert_single_movie("New Movie", 7.5, 5000, "2024-01-01")

    # 批量插入数据示例
    batch_movies = [
        {"title": "Movie 1", "rating": 8.0, "comment_count": 8000, "release_date": "2023-05-10"},
        {"title": "Movie 2", "rating": 7.8, "comment_count": 7000, "release_date": "2023-08-15"}
    ]
    batch_insert_movies(batch_movies)

    # 查询所有记录
    print("\n查询所有电影：")
    for movie in query_all_movies():
        print(f"{movie.title} ({movie.release_date}): {movie.rating}")

    # 查询2023年上映的电影
    print("\n查询2023年上映的电影：")
    for movie in query_movies_by_year(2023):
        print(f"{movie.title} ({movie.release_date}): {movie.rating}")

    # 查询蜘蛛侠电影数据
    print("\n查询蜘蛛侠电影数据：")
    spider_man = query_movie_by_title("蜘蛛侠")
    if spider_man:
        print(f"{spider_man.title} ({spider_man.release_date}): {spider_man.rating}")

    # 更新魂断蓝桥的评分
    update_movie_rating("魂断蓝桥", 9.0)

    # 删除冰雪奇缘这部电影
    delete_movie_by_title("冰雪奇缘")

    # 统计2010年出品的电影有几部
    count_2010 = count_movies_by_year(2010)
    print(f"\n2010年出品的电影数量：{count_2010} 部")

    # 分页查询，每页显示25条
    print("\n分页查询（第1页，每页25条）：")
    for movie in paginate_movies(page=1):
        print(f"{movie.title} ({movie.release_date}): {movie.rating}")

    # 导出数据到 CSV 文件
    export_csv_file_path = 'C:/Users/20342/Desktop/final/CSV/exported_movies.csv'
    export_database_to_csv(export_csv_file_path)

    db.close()