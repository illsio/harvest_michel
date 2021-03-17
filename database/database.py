import json
import sqlite3
import random, string

## Change to local paths - I couldnt fix this!!!
dbPath = 'database/chartsdb.db'
jsonPath = 'database/chart-json/{}.json'

def connect():
    con = sqlite3.connect(dbPath)
    if con:
        # get the count of tables with the name
        cur = con.cursor()
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='CHARTS' ''')

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:
            print('Table exists.')
        else:
            createTable(con)
    return con


def load(hash):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM CHARTS WHERE  hash=?", (hash,))
    result = cur.fetchone()
    if result:
        try:
            with open(result[2]) as config:
                config_json = json.load(config)
                return {
                    "db_entry": result,
                    "config": config_json
                }
        except FileNotFoundError:
            print("config not in DB")
        

    else:
        return None


def loadAll():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM CHARTS")
    results = cur.fetchall()
    return results


def saveChart(chartData):
    con = connect()
    cur = con.cursor()
    hash = createHash()
    filePath = saveFile(hash, chartData)
    sql = 'INSERT INTO CHARTS (hash, path) values(?, ?)'
    cur.execute(sql, (hash, filePath))
    con.commit()
    con.close()


def createHash():
    hash = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return hash


def createTable(con):
    cur = con.cursor()
    cur.execute("""
                CREATE TABLE if not exists CHARTS (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    hash TEXT,
                    path TEXT,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
    con.commit()

def saveFile(hash, data):
    filePath = jsonPath.format(hash)

    with open(filePath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return filePath
