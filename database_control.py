import sqlite3

from fastapi import HTTPException

def init_database():
    global con 
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS POSTS(
            ID      INTEGER     PRIMARY KEY NOT NULL,
            TITLE   TEXT                    NOT NULL,
            TIME    INTEGER                 NOT NULL,
            CONTENT TEXT                    NOT NULL
        );
        ''')
    
    con.commit()

def get_post(post_id:int):
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM POSTS WHERE ID = {post_id};").fetchone()
    if res is None:
        raise HTTPException(status_code=404, detail="Post not found")
    else:
        (_,title,time,content) = res
        return {"title":title,"time":time,"content":content}

def close_database():
    con.close()