import mysql.connector
from venv import logger


def save_data_into_DB(data):
    try:
        connection = mysql.connector.connect(
            user="root", password="root@", host="localhost"
        )
        cursor = connection.cursor()
        query = "INSERT INTO `crawl_data`.`job_data` (`Title`, `Company_Name`, `Time`, `City`, `Age`, `Sexual`, `Probation_Time`, `Work_Way`, `Job`, `Place`, `Number_Employee`, `Experience`, `Level`, `Salary`, `Education`, `Right`, `Description`, `Requirement`, `Deadline`, `Source_Picture`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in data:
            cursor.execute(query, i)
        connection.commit()
        connection.close()
    except Exception as e:
        logger.error(f"Error occurred while saving data to DB: {e}")

# Create database if not exists
def create_database_if_not_exists(my_user, my_password):
    try:
        connection = mysql.connector.connect(
            user=my_user, password=my_password, host="localhost"
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS crawl_data")
        connection.close()
    except Exception as e:
        print(f"Error occurred while creating database: {e}")

# Create table if not exists
def create_table_if_not_exists(my_user, my_password):
    try:
        connection = mysql.connector.connect(
            user=my_user, password=my_password, host="localhost", database="crawl_data"
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Title VARCHAR(255),
                Company_Name VARCHAR(255),
                Time VARCHAR(255),
                City VARCHAR(255),
                Age VARCHAR(255),
                Sexual VARCHAR(255),
                Probation_Time VARCHAR(255),
                Work_Way VARCHAR(255),
                Job VARCHAR(255),
                Place VARCHAR(255),
                Number_Employee VARCHAR(255),
                Experience VARCHAR(255),
                Level VARCHAR(255),
                Salary VARCHAR(255),
                Education VARCHAR(255),
                `Right` VARCHAR(255),
                Description VARCHAR(255),
                Requirement VARCHAR(255),
                Deadline VARCHAR(255),
                Source_Picture VARCHAR(255)
            )
        """)
        connection.close()
    except Exception as e:
        print(f"Error occurred while creating table: {e}")

def get_data_from_DB(my_user, my_password):
    try:
        create_database_if_not_exists(my_user, my_password)
        create_table_if_not_exists(my_user, my_password)
        connection = mysql.connector.connect(
            user=my_user, password=my_password, host="localhost"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM crawl_data.job_data")
        data = cursor.fetchall()
        connection.close()
        return data
    except Exception as e:
        print(f"Error occurred while retrieving data from database: {e}")
        return []
