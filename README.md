SimpleORM
=========

SimpleORM is almost too simple to be called an ORM.  Mostly it gets out of your way, and saves you time writing select, insert, update, and delete statements.

Usage
-----

After creating the connection, all you do is call it on the table you're operating against.

>>> import psycopg2
>>> from simpleorm import DBConnection

>>> conn = psycopg2.connect(user="jmelloy")
>>> db = DBConnection(conn)

By default, it returns a generator with a dict of the row.

>>> rset = db.select("library_books")
>>> for row in rset:
...     print row['id'], row['author']
20 Douglas Adams
21 Douglas Adams
26 Douglas Adams
27 Douglas Adams

You can also return the row itself:
>>> rset = db.select("library_books", return_type="rset")
>>> for row in rset:
...     print row
(20, "Dirk Gently's Holistic Detective Agency", '0671746723', 'http://ecx.images-amazon.com/images/I/51KTBFRE8DL.jpg', 283, 475, 'http://www.amazon.com/Dirk-Gentlys-Holistic-Detective-Agency/dp/0671746723', 'Pocket', 'DG 1', 'Douglas Adams')
(21, 'The Long Dark Tea-Time of the Soul', '0671742515', 'http://ecx.images-amazon.com/images/I/5144VAJXG9L.jpg', 290, 475, 'http://www.amazon.com/Long-Dark-Tea-Time-Soul/dp/0671742515', 'Pocket Books', 'DG 2', 'Douglas Adams')

Or get a JSON object with everything:
>>> db.select("library_books", where={"author":"Douglas Adams"}, select_list=['id', 'title', 'asin', 'publisher', 'series'], order="series", return_type = 'json')
{"rows": [[20, "Dirk Gently\'s Holistic Detective Agency", "0671746723", "Pocket", "DG 1"], 
[21, "The Long Dark Tea-Time of the Soul", "0671742515", "Pocket Books", "DG 2"], 
[26, "So Long, and Thanks for All the Fish", "0345479963", "Del Rey", "HH4"], 
[27, "Mostly Harmless", "0345418778", "Del Rey", "HH5"]], 
"total_rows": 4, 
"run_date": "2011-02-06 16:04:01.917889", 
"run_time": "0.006225", 
"sql": "select id, title, asin, publisher, series from library_books  where author = \'Douglas Adams\'  order by series", 
"columns": ["id", "title", "asin", "publisher", "series"]}

If you want to include a where clause, it will accept either a text clause or a dictionary with the values.

>>> rset = db.select("library_books", where={"author":"Douglas Adams"}, order="title desc")
>>> rset = db.select("library_books", where="author like 'D%Adams%' and publication_date < '1985-Jan-01'")

Joins and specific columns are easy, too:
>>> rset = db.select("library_books join library_authors using (author_id)", select_list=['library_books.id', 'library_authors.author', 'library_books.*'])

Other common methods are also included:
>>> rowcount = db.insert("library_books", {"Title":"The Long Dark Tea-Time of the Soul", "Author":"Douglas Adams"})
>>> rowcount = db.update("library_books", set_list={"publication_date":"1988"}, where={"Title":"The Long Dark Tea-Time of the Soul", "Author":"Douglas Adams"})
>>> rowcount = db.upsert("library_books", set_list={"publication_date":"1987"}, where={"Title": "Dirk Gently's Holistic Detective Agency", "Author":"Douglas Adams"})
>>> rowcount = db.delete("library_books", where={"author":"Douglas Adams"})

