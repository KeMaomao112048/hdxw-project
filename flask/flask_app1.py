from flask import Flask, render_template
from news_handle1 import connect_db, get_newsinfo
 
app = Flask(__name__)


    
@app.route('/')
def hdxw():
    db = connect_db()
    news_list, last_update_time = get_newsinfo(db)

    return render_template('news.html', news_list=news_list, last_update_time= last_update_time['crawl_time'])

if __name__ == '__main__':
    
    app.run(host="0.0.0.0",port=5000,debug=True)
