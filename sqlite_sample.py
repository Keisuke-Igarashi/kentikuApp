import sqlite3


db = sqlite3.connect('instance/flaskr.sqlite')
curs = db.cursor()

curs.execute(
    'INSERT INTO user (username, password) VALUES ("admin", "admin")'
)

db.commit()

db.close()