from flask import Flask, render_template
from news_handle2 import NewsHandle
 
app = Flask(__name__)


@app.route('/')
def hdxw():
    news = NewsHandle()
    news_list, last_update_time = news.connect_db().get_newsinfo()

    return render_template('news.html', news_list=news_list, last_update_time= last_update_time['crawl_time'])

if __name__ == '__main__':
    
    app.run(host="0.0.0.0",port=5000,debug=True)
