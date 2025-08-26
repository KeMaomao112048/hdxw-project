import mysql.connector
from mysql.connector import Error


def connect_db():
    db = None
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="112048",
            database="hdxw"
        )
        if db.is_connected():
            print("数据库连接成功")
            return db
    except Error as e:
        print(f"数据库连接错误: {e}")
        return 


def create_table(db):
    if db:
        try:
            cursor = db.cursor()
            sql = """
            CREATE TABLE IF NOT EXISTS hqu_news (
                id INT AUTO_INCREMENT PRIMARY KEY,  
                title VARCHAR(255) NOT NULL,
                link VARCHAR(255)  NOT NULL,
                crawl_time DATETIME NOT NULL,
                UNIQUE (title, link)
                )
                """
            cursor.execute(sql)
            db.commit()
            print("新闻表创建成功或已存在")
        except Error as e:
            print(f"创建表时出错: {e}")
        finally:
                cursor.close()
       

def insert_newsinfo(db, news_list, spider_time):
    try:
        cursor = db.cursor()
        # 使用INSERT IGNORE避免重复插入
        insert_sql = """
        INSERT IGNORE INTO hqu_news (title, link, crawl_time)
        VALUES (%s, %s, %s)
        """
        
        # 准备数据
        data = [(item['title'], item['link'], spider_time) for item in news_list]
        
        cursor.execute("TRUNCATE TABLE hqu_news")
        db.commit()

        # 执行批量插入
        cursor.executemany(insert_sql, data)
        db.commit()
        print(f"成功插入 {cursor.rowcount} 条新新闻")
    except Error as e:
        print(f"插入数据时出错: {e}")
        db.rollback()
    finally:
            cursor.close()
            db.close()


def get_newsinfo(db):
    if db:
        try:
            # 获取所有新闻
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT title,link FROM hqu_news ORDER BY crawl_time DESC")
            news_list=cursor.fetchall()

           # 获取最新更新时间
            cursor.execute("SELECT crawl_time FROM hqu_news ORDER BY crawl_time ASC limit 1")
            latest_update_time = cursor.fetchone()
            print(f"获取到{len(news_list)}条新闻")

            return news_list, latest_update_time
        except Error as e:
            print(f"获取新闻失败:{e}")
            return [], None
        finally:
            cursor.close()
            db.close()

