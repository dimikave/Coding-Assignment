import mysql.connector


def store_in_database(data, reinit, database_hostname, database_username, database_password, database_name):
    # Connect to the database
    conn = mysql.connector.connect(
        host=database_hostname,
        user=database_username,
        password=database_password,
        database=database_name,
    )

    # Create a cursor
    cursor = conn.cursor()

    # If you want to re initialize the table:
    if reinit == True:
        sql = "DROP TABLE results"
        cursor.execute(sql)

    # Create the table if it does not already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            gatewayEui BIGINT,
            profileId INT,
            endpointId INT,
            clusterId INT,
            attributeId INT,
            timestamp BIGINT,
            value REAL
        )
    """)


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

def read_from_database(database_hostname, database_username, database_password, database_name):
    # Connect to the database
    conn = mysql.connector.connect(
        host=database_hostname,
        user=database_username,
        password=database_password,
        database=database_name,
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