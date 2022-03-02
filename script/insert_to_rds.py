import psycopg2
from datetime import datetime
from dotenv import dotenv_values
from random import choice
import time

config = dotenv_values(".env")
USER = config.get("USER")
PASSWORD = config.get("PASSWORD")
HOST = config.get("HOST")


dsn = (
    "dbname={dbname} "
    "user={user} "
    "password={password} "
    "port={port} "
    "host={host} ".format(
        dbname="orders",
        user=USER,
        password=PASSWORD,
        port=5432,
        host=HOST,
    )
)

conn = psycopg2.connect(dsn)
print("connected")
conn.set_session(autocommit=True)
cur = conn.cursor()
cur.execute(
    "create table if not exists orders("
    "created_at timestamp,"
    "order_id integer,"
    "product_name varchar(100),"
    "value float);"
)

products = {
    "pencil": 1.2,
    "pen": 2.1,
    "rubber": 2.65,
    "ruler": 5.99,
    "scissor": 11.20,
    "notebook": 4.81,
    "pencil case": 22.44,
    "glue": 3.95,
}
idx = 0

while True:
    print(idx)
    idx += 1
    created_at = datetime.now().isoformat()
    product_name, value = choice(list(products.items()))
    cur.execute(
        f"insert into orders values ('{created_at}', {idx}, '{product_name}', {value})"
    )
    time.sleep(0.2)
