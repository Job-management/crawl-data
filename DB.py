import mysql.connector
from venv import logger

def save_data_into_DB(data):
    try:
        connection = mysql.connector.connect(user='root', password='Trinh1406@', host='localhost')
        cursor = connection.cursor()
        query = "INSERT INTO `crawl_data`.`job_data` (`Title`, `Company_Name`, `Time`, `City`, `Age`, `Sexual`, `Probation_Time`, `Work_Way`, `Job`, `Place`, `Number_Employee`, `Experience`, `Level`, `Salary`, `Education`, `Right`, `Description`, `Requirement`, `Deadline`, `Source_Picture`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in data:
            cursor.execute(query, i)
        connection.commit()
        connection.close()
    except Exception as e:
        logger.error(f"Error occured while saving data to DB: {e}")

def get_data_from_DB():
    try:
        connection = mysql.connector.connect(user='root', password='Trinh1406@', host='localhost')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM crawl_data.job_data")
        data = cursor.fetchall()
        connection.close()
        return data
    except Exception as e:
        print(f"Error occurred while retrieving data from database: {e}")
        return []