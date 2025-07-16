import psycopg2
import pandas as pd
import json

def GetCustomerInfo(id):
    conn = None
    dataTable = pd.DataFrame()
    try:
        with open('appsettings.json', 'r') as f:
            config = json.load(f)
        db_config = config["ConnectionStrings"]["DefaultConnection"]

        conn = psycopg2.connect(
            host=db_config["host"],
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"]
        )

        query = "SELECT id FROM Customer WHERE id = %s"
        data = pd.read_sql(query, conn, params=(id,))
        dataTable = data.astype(
            {
                "id": str,
                "name": str
            }
        )

    except Exception as e:
        print(f"error: {e}")

    finally:
        if conn:
            conn.close()

    return dataTable