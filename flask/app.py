from flask import Flask, render_template
from database import get_connection
 
app = Flask(__name__)


    
@app.route('/')
def hdxw():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT title,link FROM hqu_news ORDER BY crawl_time DESC")
    news_list=cursor.fetchall()

    cursor.execute("SELECT crawl_time FROM hqu_news ORDER BY crawl_time ASC limit 1")
    last_update_time = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template('news.html', news_list=news_list, last_update_time= last_update_time)

if __name__ == '__main__':
    
    app.run(host="0.0.0.0",port=5000,debug=True)
