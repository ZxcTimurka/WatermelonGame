import sqlite3


def create_table():
    con = sqlite3.connect('score.db')
    with con:
        cursor = con.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scores(
                        score INTEGER PRIMARY KEY,
                        date TEXT
                    )
                ''')


def add_score(score, date):
    con = sqlite3.connect('score.db')
    with con:
        data = con.execute("select count(*) from sqlite_master where type='table' and name='goods'")
        for row in data:
            if row[0] == 0:
                create_table()
                with con:
                    cursor = con.cursor()
                    cursor.execute('''
                            INSERT INTO scores(score, date) VALUES(?, ?)
                        ''', (score, date))
                    con.commit()
            else:
                with con:
                    cursor = con.cursor()
                    cursor.execute('''
                            NSERT INTO scores(score, date) VALUES(?, ?)
                        ''', (score, date))
                    con.commit()
