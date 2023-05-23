import mariadb
import sys

try:
    conn = mariadb.connect(
        user="android",
        password="android",
        host="172.17.10.30",
        port=3306,
        database="android")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()