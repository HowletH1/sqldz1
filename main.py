from flask import Flask, jsonify
from utils import get_one, get_all

app = Flask(__name__)


@app.get('/movie/<title>')
def get_by_title(title: str):
    query = f"""
        SELECT * FROM netflix
        WHERE  title = '{title}'
        ORDER BY date_added desc
        """

    que_res = get_one(query)

    if que_res is None:
        return jsonify(status=404)

    movie = {
        "title": que_res["title"],
        "country": que_res["country"],
        "release_year": que_res["release_year"],
        "genre": que_res["listed_in"],
        "description": que_res["description"]
    }

    return jsonify(movie)


@app.get('/movie/<year1>/to/<year2>')
def get_by_year(year1: str, year2: str):
    query = f"""
    SELECT * from netflix
    WHERE release_year BETWEEN  {year1} and {year2}
    LIMIT 100
    """

    res = []

    for item in get_all(query):
        res.append(
            {
                'title': item['title'],
                'release_year': item['release_year']
            }
        )

    return jsonify(res)


@app.get('/movie/rating/<value>')
def get_by_rating(value: str):
    query = """
    SELECT * from netflix
    """

    if value == "children":
        query += 'WHERE rating = "G"'
    elif value == 'family':
        query += 'WHERE rating = "G" or rating = "PG" or rating = "PG-13"'
    elif value == 'adult':
        query += 'WHERE rating = "R"  or rating = "PG-17"'
    else:
        return jsonify(status=400)

    res = []

    for item in get_all(query):
        res.append(
            {
                'title': item['title'],
                'rating': item['rating'],
                'description': item['description']
            }
        )
    return jsonify(res)


@app.get('/genre/<genre>')
def get_by_genre(genre: str):
    query = f"""
    SELECT * from netflix
    WHERE listed_in LIKE '%{genre}%'
    ORDER BY date_added desc
    limit 10
    """

    res = []

    for item in get_all(query):
        res.append(
            {
                'title': item['title'],
                'description': item['description']
            }
        )

    return jsonify(res)


app.run(debug=True)
