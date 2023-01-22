import sqlite3


def get_all(query: str):
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row

        res = []

        for item in conn.execute(query).fetchall():
            res.append(dict(item))

        return res


def get_one(query: str):
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row
        res = conn.execute(query).fetchone()
        if res is None:
            return None
        else:
            return dict(res)


def get_movie(type_movie, release_year, listed_in):
    query = f"""
    SELECT title, description FROM netflix
    WHERE  "type" = '{type_movie}'
    AND release_year = '{release_year}'
    AND listed_in = '%{listed_in}%'
    """

    res = []

    for item in get_all(query):
        res.append(
            {
                'title': item['title'],
                'description': item['description']
            }
        )

    return res


def search_cast(name1: str = 'Jack Black', name2: str = 'Dustin Hoffman'):
    query = f"""
    SELECT * FROM netflix
    WHERE netflix."cast" like '%Jack Black%' and netflix."cast" like '%Dustin Hoffman%'
    """
    cast = []
    set_cast = set()
    res = get_all(query)

    for item in res:
        for actor in item['cast'].split('.'):
            cast.append(actor)

    for actor in cast:
        if cast.count(actor) > 2:
            set_cast.add(actor)

    return list(set_cast)

