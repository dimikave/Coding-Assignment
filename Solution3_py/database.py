import mysql.connector

class Database:
    def __init__(self, hostname, username, password, database):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database


    def store_results(self, data, flag, reinit=True):
        # Connect to the database
        connection = mysql.connector.connect(
            host=self.hostname,
            user=self.username,
            password=self.password,
            database=self.database
        )

        # Create a cursor object
        cursor = connection.cursor()

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


        if flag:
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
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

    def read_results(self):
        # Connect to the database
        connection = mysql.connector.connect(
            host=self.hostname,
            user=self.username,
            password=self.password,
            database=self.database
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Create the SQL query
        query = "SELECT * FROM results"

        # Execute the query
        cursor.execute(query)

        # Fetch all results
        results = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return results
