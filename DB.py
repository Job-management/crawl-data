import mysql.connector
from venv import logger


def save_data_into_DB(data):
    try:
        connection = mysql.connector.connect(
            user="root", password="root@", host="localhost", database="job-management"
        )
        cursor = connection.cursor()
        query = "INSERT INTO `job-management`.`crawl_data` (`title`, `company`, `time`, `city`, `age`, `sexual`, `probationTime`, `workWay`, `job`, `place`, `numberEmployees`, `experience`, `level`, `salary`, `education`, `right`, `description`, `requirements`, `deadline`, `images`, `link`, `type`, `major_category_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for i in data:
            cursor.execute(query, i)
        connection.commit()
        connection.close()
    except Exception as e:
        logger.error(f"Error occurred while saving data to DB: {e}")

def is_duplicate_data(link):
    try:
        connection = mysql.connector.connect(
            user="root", password="root@", host="localhost", database="job-management"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM `crawl_data` WHERE `link` = %s"
        cursor.execute(query, (link,))
        data = cursor.fetchall()
        connection.close()
        return len(data) > 0
    except Exception as e:
        print(f"Error occurred while retrieving data from database: {e}")
        return False

def get_data_from_DB(my_user, my_password):
    try:
        # create_database_if_not_exists(my_user, my_password)
        # create_table_if_not_exists(my_user, my_password)
        connection = mysql.connector.connect(
            user="root", password="root@", host="localhost"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `job-management`.`crawl_data`")
        data = cursor.fetchall()
        connection.close()
        return data
    except Exception as e:
        print(f"Error occurred while retrieving data from database: {e}")
        return []

# Create database if not exists
def create_database_if_not_exists(my_user, my_password):
    try:
        connection = mysql.connector.connect(
            user="root", password="root@", host="localhost", database="job-management"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `job-management`.`crawl_data`")
        data = cursor.fetchall()
        connection.close()
        return data
    except Exception as e:
        print(f"Error occurred while retrieving data from database: {e}")
        return []
