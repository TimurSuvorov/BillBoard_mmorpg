import os

import psycopg2

conn_obj = psycopg2.connect(
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    port='5432'
)

cur = conn_obj.cursor()
cur.execute('SELECT * from django_content_type;')
cur.execute('TRUNCATE django_content_type CASCADE;')
cur.execute('SELECT * from django_content_type;')
print(r'INFO: "django_content_type" cleared. Now you can load dump by loaddata')
conn_obj.commit()
conn_obj.close()
