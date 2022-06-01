import csv

from sqlalchemy import insert

from src.database.tables import metadata, posts
from src.dependencies import get_engine
from src.post.models import PostRequestV1
from src.search.service import add_to_index

from pathlib import Path
import os

filename = "fixtures/posts.csv"

BASE_DIR = Path(__file__).resolve().parent

# print("in create_data.py")
# print(BASE_DIR)

db = get_engine()
metadata.drop_all(db)
metadata.create_all(db)
conn = db.connect()

with open(os.path.join(BASE_DIR, filename), newline='') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        # print(row['text'], row['created_date'], row['rubrics'])
        # print(row)
        ins = insert(posts).values(**row)
        conn.execute(ins)
        post = PostRequestV1(
            id=i,
            text=row["text"]
        )
        add_to_index("posts", post)
        print(f"processed row {i}")

        # if i > 10:
        #     break

conn.commit()
conn.close()
