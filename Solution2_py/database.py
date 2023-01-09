import mysql.connector
import pandas as pd 

def store_in_database(data):
    # Connect to the database
    conn = mysql.connector.connect(
        host="candidaterds.n2g-dev.net",
        user="cand_62cm",
        password="3ITMjTgArIDmesgX",
        database="cand_62cm",
    )
    print(data['timestamp'])
    # Create a cursor
    cursor = conn.cursor()

    sql = "DROP TABLE results"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS results (gatewayEui BIGINT, profileId INTEGER, endpointId INTEGER, clusterId INTEGER, attributeId INTEGER, timestamp BIGINT, value REAL)"
    cursor.execute(sql)

    print('oof')
    # Insert the data into the table
    sql = "INSERT INTO results (gatewayEui, profileId, endpointId, clusterId, attributeId, timestamp, value) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # sql = "INSERT INTO results (timestamp, value) VALUES (%s, %s)"

    values = (
        data["gatewayEui"],
        data["profileId"],
        data["endpointId"],
        data["clusterId"],
        data["attributeId"],
        data["timestamp"],
        data["value"],
    )
    cursor.execute(sql, values)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def read_from_database():
    # Connect to the database
    conn = mysql.connector.connect(
        host="candidaterds.n2g-dev.net",
        user="cand_62cm",
        password="3ITMjTgArIDmesgX",
        database="cand_62cm",
    )

    # Create a cursor
    cursor = conn.cursor()

    # Select all the records from the table
    sql = "SELECT * FROM results"
    cursor.execute(sql)

    # Fetch the records
    records = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return records