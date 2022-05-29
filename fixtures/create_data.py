import csv

from sqlalchemy import insert

from src.database.tables import metadata, posts
from src.dependencies import get_engine

filename = "posts.csv"

db = get_engine()
metadata.drop_all(db)
metadata.create_all(db)
conn = db.connect()

with open(filename, newline='') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        # print(row['text'], row['created_date'], row['rubrics'])
        # print(row)
        ins = insert(posts).values(**row)
        conn.execute(ins)
        # if i > 10:
        #     break

conn.commit()
conn.close()
