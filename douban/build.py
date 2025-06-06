from peewee import *
import pymysql

# 注册 MySQL 驱动
pymysql.install_as_MySQLdb()

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
    # 先连接到 MySQL 服务器（不指定数据库）
    mysql_server = MySQLDatabase(None)
    mysql_server.init(
        database='mysql',  # 连接到默认的 mysql 数据库
        **DB_CONFIG
    )
    
    try:
        mysql_server.connect()
        with mysql_server.atomic():
            # 执行创建数据库的语句
            mysql_server.execute_sql(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"数据库 '{db_name}' 已创建或已存在")
    except Exception as e:
        print(f"创建数据库时出错: {e}")
        raise
    finally:
        mysql_server.close()

# 配置数据库连接
db = MySQLDatabase(
    'test_db',
    **DB_CONFIG
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
    try:
        # 先创建数据库（如果不存在）
        create_database_if_not_exists('test_db')
        
        # 再连接到数据库并创建表
        db.connect()
        db.create_tables([Movie])
        print("数据库初始化完成")
    except Exception as e:
        print(f"初始化数据库时发生错误: {e}")

# 其他函数保持不变...