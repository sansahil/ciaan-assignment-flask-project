import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres"
    )
    print("Connection successful!")
except psycopg2.OperationalError as e:
    print("Unable to connect to the database:")
    print(e)

