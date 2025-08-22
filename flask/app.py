from flask import Flask, render_template
from database import get_connection
 
app = Flask(__name__)


    
@app.route('/hdxw')
def hdxw():
    db = get_connection()
    cursor = db.cursor()
    db.close()
    news = cursor.execute("SELECT title,link FROM hdxw").fetchall()
    last_update_time = cursor.execute("SELECT crawl_time FROM hdxw ORDER BY crawl_time DESC").fetchone()
    news_list = [dict(row) for row in news]
    return render_template('news.html', news_list=news_list, last_update_time= last_update_time)

if __name__ == '__main__':
    
    app.run(debug=True)
