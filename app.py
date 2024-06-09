from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

@app.route("/")
def home():
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

if __name__ == "__main__":
    app.run(debug=True)