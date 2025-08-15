from bs4 import BeautifulSoup
import requests

url = 'https://news.hqu.edu.cn/'

response = requests.get(url)
response.encoding = 'utf-8'

news_list = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.find_all('a')
    for new in news:
        title = new.get_text()
        link = new.get('href')
        if not link.startswith('http'):
                link = f"https://news.hqu.edu.cn/{link}"
        news_list.append({'title': title, 'link': link})
else:
    print('Request failed.status code:',response.status_code)

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hdxw')
def hdxw():
    return render_template('news.html', news_list=news_list)

if __name__ == '__main__':
    app.run(debug=True)


