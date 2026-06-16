import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="riscv_knowledge_db",
    user="totallynotsatnam",
    password="riscv123"
)

cur = conn.cursor()

cur.execute("SELECT version();")

print(cur.fetchone())

cur.close()
conn.close()