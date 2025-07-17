import psycopg2
import pandas as pd
import json
from datetime import datetime

def GetCustomerInfo(id, startDate=None, endDate=None):
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

        query = "SELECT id, name, created_at FROM Customer WHERE id = %s"
        params = [id]

        if startDate:
            if not endDate:
                endDate = datetime.now().strftime('%d-%m-%Y')
            query += " AND created_at BETWEEN %s AND %s"
            params.extend([startDate, endDate])

        data = pd.read_sql(query, conn, params=params)
        dataTable = data.astype({
            "id": str,
            "name": str
        })

    except Exception as e:
        print(f"error: {e}")

    finally:
        if conn:
            conn.close()

    return dataTable
