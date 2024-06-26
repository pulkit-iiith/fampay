import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime
import constants


class Database_Handler:
    # Define MySQL connection parameters
    load_dotenv()
    config = {
            'user': os.getenv('MYSQL_USER'),
            'password': os.getenv('MYSQL_PASSWORD'),
            'host': os.getenv('MYSQL_HOST'),
            'database': os.getenv('MYSQL_DATABASE'),
            'port': os.getenv('MYSQL_PORT', '3306'),
            'auth_plugin':'mysql_native_password'
        }    

    def make_connection_and_insert_data(self,data):

        # Establish connection to MySQL
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()

        # Create a table to store video data if not exists
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS videos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title_publishing_datetime VARCHAR(255) UNIQUE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            publishing_datetime DATETIME NOT NULL,
            thumbnails_default TEXT,
            thumbnails_medium TEXT,
            thumbnails_high TEXT
        );
        '''
        cursor.execute(create_table_query)


        # Define the SQL query to check if title_publishing_datetime already exists
        check_query = "SELECT COUNT(*) FROM videos WHERE title_publishing_datetime = %s"

        # Define the SQL query to insert data
        insert_query = '''
        INSERT INTO videos (title_publishing_datetime, title, description, publishing_datetime, thumbnails_default, thumbnails_medium, thumbnails_high)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        # Extract and insert data
        for item in data:
            video_title = item['title']
            publishing_datetime = item['publishing_datetime']
            title_publishing_datetime = f"{video_title}_{publishing_datetime}"  # Combine title and publishTime
            cursor.execute(check_query, (title_publishing_datetime,))
            result = cursor.fetchone()[0]
            if result == 0:  # If title_publishTime does not exist, insert the record
                video_data = (
                    title_publishing_datetime,
                    video_title,
                    item['description'],
                    item['publishing_datetime'],
                    item['thumbnails']['default'],
                    item['thumbnails']['medium'],
                    item['thumbnails']['high']
                )
                cursor.execute(insert_query, video_data)
                connection.commit()
                print(f"Inserted: {video_title}")
            else:
                print(f"Skipping duplicate entry: {video_title}")

        # Close connection
        cursor.close()
        connection.close()

    # Function to execute SQL query and fetch video data
    def fetch_videos(self,page, per_page):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()

        # Calculate offset
        offset = (page - 1) * per_page

        # Execute SQL query
        sql_query = f"SELECT * FROM videos ORDER BY publishing_datetime DESC LIMIT {per_page} OFFSET {offset};"
        cursor.execute(sql_query)

        # Fetch data
        video_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return video_data    

    # Function to execute SQL query and fetch video data
    def search_videos(self,title_query, description_query):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()

        # Construct SQL query with wildcard characters for partial matching
        sql_query = "SELECT * FROM videos WHERE title LIKE %s OR description LIKE %s"
        params = ('%' + title_query + '%', '%' + description_query + '%') if title_query and description_query else \
                 ('%' + title_query + '%', '%' + title_query + '%') if title_query else \
                 ('%' + description_query + '%', '%' + description_query + '%')
        
        # Execute SQL query
        cursor.execute(sql_query, params)

        # Fetch data
        video_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return video_data
