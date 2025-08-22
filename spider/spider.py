from bs4 import BeautifulSoup
import requests,time
from database import insert_news, create_tables

url = 'https://news.hqu.edu.cn/'
last_update_time = ''
last_crawl_time = 0
CRAWL_INTERVAL = 3600  # 爬取间隔时间，单位：秒

def crawl_news():
    global  last_crawl_time, last_update_time
    try:
        response = requests.get(url,timeout=10)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            current_time = time.time()
            if current_time - last_crawl_time > CRAWL_INTERVAL:
                last_crawl_time = current_time
                last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_crawl_time))
                soup = BeautifulSoup(response.text, 'lxml')
                news = soup.find_all('a')

                news_list = []
                for new in news:
                    title = new.get_text()
                    link = new.get('href')
                    # 过滤掉无效的新闻
                    if title and link and len(title) > 5:
                        # 补全链接
                        if not link.startswith('http'):
                            link = f"https://news.hqu.edu.cn/{link}"
                        news_list.append({'title': title, 'link': link})
                
                # 保存到数据库
                insert_news(news_list, last_update_time)
        else:
            print('Request failed.status code:',response.status_code)
    except Exception as e:
        print(f'爬取错误: {str(e)}')




if __name__ == '__main__':
    create_tables()
    while True:
        crawl_news()
        # 等待指定的时间间隔
        time.sleep(CRAWL_INTERVAL)
