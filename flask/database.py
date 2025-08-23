import mysql.connector
from mysql.connector import Error

def get_connection():
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
        return None

def create_tables():
    db = get_connection()
    if db:
        try:
            cursor = db.cursor()
            #cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            #cursor.execute(f"USE {DB_CONFIG['database']}")
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
            if db.is_connected():
                cursor.close()
                db.close()
       

def insert_news(news_items, crawl_time):
    db = get_connection()
    try:
        cursor = db.cursor()
        # 使用INSERT IGNORE避免重复插入
        insert_sql = """
        INSERT IGNORE INTO hqu_news (title, link, crawl_time)
        VALUES (%s, %s, %s)
        """
        
        # 准备数据
        data = [(item['title'], item['link'], crawl_time) for item in news_items]
        
        # 执行批量插入
        cursor.executemany(insert_sql, data)
        db.commit()
        print(f"成功插入 {cursor.rowcount} 条新新闻")
    except Error as e:
        print(f"插入数据时出错: {e}")
        db.rollback()
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

