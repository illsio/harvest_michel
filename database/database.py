import sqlite3
import urllib.request, json

## Change to local paths - I couldnt fix this!!!
dbPath = 'database/alerts.db'
jsonPath = 'database/example-json/{}.json'


def create():
    con = sqlite3.connect(dbPath)
    if con:
        # get the count of tables with the name
        cur = con.cursor()
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='alerts' ''')

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:
            None
        else:
            createAltertsTable(con)
            createMetaTable(con)
    return con


def countAll():
    con = create()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM alerts")
    count = cur.fetchall()
    return count



def fetchAll():
    con = create()
    cur = con.cursor()
    cur.execute("SELECT * FROM alerts")
    return cur.fetchall()


def createAltertsTable(con):
    cur = con.cursor()
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS alerts (
                        type VARCHAR NULL,
                        [geometry.type] VARCHAR NULL,
                        [geometry.coordinates] JSON NULL,
                        [properties.mmlid] VARCHAR NULL,
                        [properties.str] VARCHAR NULL,
                        [properties.hsnr] INT NULL,
                        [properties.zus] VARCHAR NULL,
                        [properties.plz] VARCHAR NULL,
                        [properties.ort] VARCHAR NULL,
                        [properties.zust] INT NULL,
                        [properties.start] REAL NULL,
                        [properties.ende] REAL NULL,
                        [properties.statu] VARCHAR NULL,
                        [properties.oeff] VARCHAR NULL,
                        [properties.beschr] VARCHAR NULL,
                        [properties.pic] VARCHAR NULL,
                        [properties.rueck] VARCHAR NULL,
                        [properties.kat] INT NULL,
                        [properties.kat_text] VARCHAR NULL,
                        [properties.skat] INT NULL,
                        [properties.skat_text] VARCHAR NULL,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """)
    con.commit()


def saveAlertEntry(data):
    con = create()
    cur = con.cursor()
    sql = "INSERT INTO alerts (type, [geometry.type], [geometry.coordinates], [properties.mmlid], [properties.str], [properties.mmlid], [properties.zus], [properties.plz], [properties.ort], [properties.zust], " \
            " [properties.start], [properties.ende], [properties.statu], [properties.oeff], [properties.beschr], [properties.pic], [properties.rueck], [properties.kat], [properties.kat_text], [properties.skat], [properties.skat_text]) " \
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

    newEntries = 0
    existingEntries = 0

    for feature in data['features']:
        mmlid = feature["properties"]["mmlid"]
        existingEntry = loadAltertEntry(mmlid)
        if (existingEntry):
            if (existingEntry[12] != feature["properties"]["statu"]):
                print("status changed")
                commitNewEntry(con, cur, sql, feature)

        if(feature["properties"]["oeff"] != 'TRUE'):
            print("not done yet: " + mmlid)

        if not(existingEntry):
            commitNewEntry(con, cur, sql, feature)
            print("New elements " + mmlid)
            newEntries = newEntries + 1
        else:
            existingEntries = existingEntries + 1
            print("Element exists: " + mmlid)

    saveChart(newEntries, existingEntries)
    con.close()

def commitNewEntry(con, cur, sql, feature):
    cur.execute(sql, (
        feature["type"],
        feature["geometry"]["type"],
        json.dumps(feature["geometry"]["coordinates"]),
        feature["properties"]["mmlid"],
        feature["properties"]["str"],
        feature["properties"]["hsnr"],
        feature["properties"]["zus"],
        feature["properties"]["plz"],
        feature["properties"]["ort"],
        feature["properties"]["zust"],
        feature["properties"]["start"],
        feature["properties"]["ende"],
        feature["properties"]["statu"],
        feature["properties"]["oeff"],
        feature["properties"]["beschr"],
        feature["properties"]["pic"],
        feature["properties"]["rueck"],
        feature["properties"]["kat"],
        feature["properties"]["kat_text"],
        feature["properties"]["skat"],
        feature["properties"]["skat_text"]
    ))
    con.commit()

def loadJSON():
    with urllib.request.urlopen("https://geoportal-hamburg.de/lgv-config/anliegen_extern.json") as url:
        data = json.loads(url.read().decode())
        return  data


def loadAltertEntry(mmlid):
    con = create()
    cur = con.cursor()
    #For multiple entries it only returns the latest
    cur.execute("SELECT * FROM alerts WHERE [properties.mmlid]=? ORDER BY Timestamp DESC LIMIT 1", (mmlid,))
    result = cur.fetchone()
    if result:
        return result
    else:
        return None



def createMetaTable(con):
    cur = con.cursor()
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS meta (
                        newEntries INT NULL,
                        existingEntries INT NULL,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                """)
    con.commit()


def saveChart(newEntries, existingEntries):
    print("New elements: " + str(newEntries) + ", existing elements: " + str(existingEntries) )
    con = create()
    cur = con.cursor()
    sql = 'INSERT INTO meta (newEntries, existingEntries) values(?, ?)'
    cur.execute(sql, (newEntries, existingEntries))
    con.commit()
    con.close()
