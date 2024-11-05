import pymysql
import os



class DatabaseManager:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")

    def connect(self):
        """
        Establish a connection to the database.
        """
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def add_email(self, email_address, country, city, work_address, home_address, arrival_time):
        """
        Adds an email with all the information to the database.
        """
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO emails (email_address, country, city, home_address, work_address, arrival_time)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (email_address, country, city, home_address, work_address, arrival_time))
                connection.commit()
                return True
        except Exception as e:
            return False
        finally:
            connection.close()

    def remove_email(self, email_address):
        """
        Removes an email from the database.
        """
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM emails WHERE email_address = %s"
                cursor.execute(sql, (email_address,))
                connection.commit()
                print("Email removed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()

    def get_emails(self):
        """
        Retrieves all emails and associated details from the database.
        """
        connection = self.connect()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # SQL query to select all user data
                sql = """
                SELECT email_address, country, city, home_address, work_address, arrival_time 
                FROM emails
                """
                cursor.execute(sql)
                result = cursor.fetchall()  # Fetch all rows as a list of dictionaries
                return result
        except Exception as e:
            print(f"An error occurred while fetching emails: {e}")
            return []
        finally:
            connection.close()


    def email_exists(self, email_address):
        """
        Checks if an email exists in the database.
        """
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM emails WHERE email_address = %s"
                cursor.execute(sql, (email_address,))
                result = cursor.fetchone()
                return result[0] > 0  # Returns True if email exists
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            connection.close()
