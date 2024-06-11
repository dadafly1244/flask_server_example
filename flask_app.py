from flask import Flask, render_template, request, redirect, url_for
import requests
import random
import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.title} {self.artist} 추천 by {self.username}'

with app.app_context():
    db.create_all()

@app.route("/lotto")
def lotto():
    name = "양다영"
    lotto = [16, 18, 20, 23, 32, 43]

    def generate_lotto_numbers():
        numbers = random.sample(range(1, 46), 6)
        return sorted(numbers)

    random_lotto = generate_lotto_numbers()

    def count_common_elements(list1, list2):
        common_elements = set(list1) & set(list2)
        return len(common_elements)

    common_count = count_common_elements(lotto, random_lotto)

    context = {
        "name": name,
        "lotto": lotto,
        "random_lotto": random_lotto,
        "common_count": common_count,
    }

    return render_template("index.html", data=context)


@app.route("/mypage")
def mypage():
    return "This is My Page!"

@app.route("/movie")
def movie():
    query = request.args.get('query') # 검색어
    URL = f"http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=f5eef3421c602c6cb7ea224104795888&movieNm={query}" # URL

    res = requests.get(URL)
    rjson = res.json()
    movie_list = rjson["movieListResult"]["movieList"]
		
    return render_template("movie.html", data=movie_list)

@app.route("/answer")
def answer():

    if request.args.get('query'):
        query = request.args.get('query')
    else:
        query = '20230601'    

    URL = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key=f5eef3421c602c6cb7ea224104795888&targetDt={query}"

    res = requests.get(URL)

    rjson = res.json()
    movie_list = rjson.get("boxOfficeResult").get("weeklyBoxOfficeList")

    return render_template("answer.html", data=movie_list)

@app.route("/")
def home():
    name = '양다영'
    motto = "행복해서 웃는게 아니라 웃어서 행복합니다."

    context = {
        "name": name,
        "motto": motto,
    }
    return render_template('motto.html', data=context)

@app.route("/music/")
def music():
    song_list = Song.query.all()
    return render_template('music.html', data=song_list)

@app.route("/music/<username>/")
def render_music_filter(username):
    filter_list = Song.query.filter_by(username=username).all()
    return render_template('music.html', data=filter_list)

@app.route("/iloveyou/<name>/")
def iloveyou(name):
    motto = f"{name}야 난 너뿐이야!"

    context = {
        'name': name,
        'motto': motto,
    }
    return render_template('motto.html', data=context)

@app.route("/music/create/")
def music_create():
    #form에서 보낸 데이터 받아오기
    username_receive = request.args.get("username")
    title_receive = request.args.get("title")
    artist_receive = request.args.get("artist")
    image_receive = request.args.get("image_url")

    # 데이터를 DB에 저장하기
    song = Song(username=username_receive, title=title_receive, artist=artist_receive, image_url=image_receive)
    db.session.add(song)
    db.session.commit()
    return redirect(url_for('render_music_filter', username=username_receive))

@app.route("/music/delete", methods=["POST"])
def music_delete():
    song_have_to_delete = request.json.get("id")
    song = Song.query.get(song_have_to_delete)
    if song:
        db.session.delete(song)
        db.session.commit()
        
    song_list = Song.query.all()
    return render_template('music.html', data=song_list)
if __name__ == "__main__":
    app.run(debug=True)