import psycopg2
import traceback

try:
    conn = psycopg2.connect(
        dbname="vendas_db",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )
    print("✅ Conexão com PostgreSQL OK!")
except Exception as e:
    print("❌ ERRO DE CONEXÃO!")
    traceback.print_exc()
