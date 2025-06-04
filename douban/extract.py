from peewee import *
import pymysql

# 注册 MySQL 驱动
pymysql.install_as_MySQLdb()

# 配置数据库连接
db = MySQLDatabase(
    'test_db',
    host='localhost',
    port=3306,
    user='root',
    password='password',
    charset='utf8mb4'
)

# 定义模型
class BaseModel(Model):
    class Meta:
        database = db

class Movie(BaseModel):
    title = CharField(max_length=100)
    rating = FloatField()
    comment_count = IntegerField()
    release_date = DateField(null=True)

    class Meta:
        table_name = 'movies'

# 数据库操作函数
def init_db():
    db.connect()
    db.create_tables([Movie])
    print("数据库初始化完成")

def add_movie(title, rating, comment_count, release_date=None):
    try:
        with db.atomic():
            movie = Movie.create(
                title=title,
                rating=rating,
                comment_count=comment_count,
                release_date=release_date
            )
            return movie
    except IntegrityError:
        print(f"电影 '{title}' 已存在")
        return None

def get_high_rating_movies(min_rating=8.5):
    return Movie.select().where(Movie.rating >= min_rating)

if __name__ == "__main__":
    init_db()
    
    # 添加测试数据
    add_movie("Inception", 8.8, 150000, "2010-07-16")
    add_movie("The Dark Knight", 9.0, 250000, "2008-07-18")
    
    # 查询高分电影
    print("高分电影列表:")
    for movie in get_high_rating_movies():
        print(f"{movie.title} ({movie.release_date}): {movie.rating}")