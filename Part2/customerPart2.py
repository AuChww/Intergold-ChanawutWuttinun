import psycopg2
import pandas as pd
import json

def GetCustomerInfo(id):
    dataTable = pd.DataFrame()
    try:
        with open('appsettings.json', 'r') as f:
            config = json.load(f)
        db_config = config["ConnectionStrings"]["DefaultConnection"]

        with psycopg2.connect(
            host=db_config["host"],
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"]
        ) as conn:
            conn.autocommit = True

            query = "SELECT id, name, created_at FROM Customer WHERE id = %s"
            params = [id]

            data = pd.read_sql(query, conn, params=params)

            dataTable = data.astype({
                "id": str,
                "name": str
            })

    except Exception as e:
        print(f"error: {e}")

    return dataTable