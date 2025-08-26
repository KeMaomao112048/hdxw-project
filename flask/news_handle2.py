import mysql.connector
from mysql.connector import Error


class NewsHandle:
    def __init__(self):
        self.db = None
        self.news_list = []
        self.latest_update_time = None


    def connect_db(self):
        try:    
            self.db = mysql.connector.connect(
                host="mysql",
                user="root",
                password="112048",
                database="hdxw"
            )
            if self.db.is_connected():
                print("数据库连接成功！")
            return self
        except Error as e:
            print(f"数据库连接失败:{e}")
            return
        

    def create_table(self):
        if self.db:
            try:
                cursor = self.db.cursor()
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
                self.db.commit()
                print("创建新闻表成功！或已经存在！")
                return self
            except Error as e:
                print(f"创建新闻表失败:{e}")
                return
            finally:
                cursor.close()
    

    def insert_newsinfo(self, news_list, spider_time):
        if self.db:
            try:
                cursor = self.db.cursor()
                 # 使用INSERT IGNORE避免重复插入
                insert_sql = """
                INSERT IGNORE INTO hqu_news (title, link, crawl_time)
                VALUES (%s, %s, %s)
                """
                 # 准备数据
                data = [(item['title'], item['link'], spider_time) for item in news_list]
                
                cursor.execute("TRUNCATE TABLE hqu_news")
                self.db.commit()
                
                # 执行批量插入
                cursor.executemany(insert_sql, data)
                self.db.commit()
                print(f"成功插入 {cursor.rowcount} 条新新闻")
                return self
            except Error as e:
                print(f"插入新闻失败:{e}")
                return
            finally:
                cursor.close()
                self.db.close()

   
    def get_newsinfo(self):
        if self.db:
            try:
                # 获取所有新闻
                cursor = self.db.cursor(dictionary=True)
                cursor.execute("SELECT title,link FROM hqu_news ORDER BY crawl_time DESC")
                self.news_list=cursor.fetchall()

                # 获取最新更新时间
                cursor.execute("SELECT crawl_time FROM hqu_news ORDER BY crawl_time ASC limit 1")
                self.latest_update_time = cursor.fetchone()
                print(f"获取到{len(self.news_list)}条新闻")

                return self.news_list, self.latest_update_time
            except Error as e:
                print(f"获取新闻失败:{e}")
                return [], None
            finally:
                cursor.close()
                self.db.close()