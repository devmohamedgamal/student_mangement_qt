import mysql.connector
import sqlite3

class ConnectDatabase:
    def __init__(self):
        self._host = "127.0.0.1"
        self._port = 3306
        self._user = "root"
        self._password = "root"
        self._database = "ds_students"
        self.con = None
        self.cursor = None


    def connect_dp(self):
            self.con = mysql.connector.connect(
                host=self._host,
                port = self._port,
                user=self._user,
                password=self._password,
                database=self._database
            )

            self.cursor = self.con.cursor(dictionary=True)

    def add_info(self,student_id,first_name,last_name,state,city,email_address):
            # connect to the database
            self.connect_dp()

            # insert data into the table
            sql = f"""
            INSERT INTO student_info (studentId, firstName, lastName, state, city, emailAddress)
            VALUES ('{student_id}', '{first_name}', '{last_name}', '{state}', '{city}', '{email_address}')
            """

            try:
                #Execute the sql query for adding info
                self.cursor.execute(sql)
                self.con.commit()

            except Exception as E:
                self.con.rollback()
                return E
            
            finally:
                # Close the database connection
                self.cursor.close()
                self.con.close()    

    def loadData(self):
        # connect to the database
        self.connect_dp()
        
        sql = "SELECT * FROM ds_students.student_info LIMIT 50"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
            
    def update_info(self, student_id, first_name, last_name, state, city, email_address):
            # connect to the database
            self.connect_dp()

            sql = f"""
            UPDATE student_info
            SET firstName = '{first_name}', lastName = '{last_name}', state = '{state}', city = '{city}', emailAddress = '{email_address}'
            WHERE studentId = '{student_id}';
            """

            try:
                # Execute the sql query for updating info
                self.cursor.execute(sql)
                self.con.commit()
            except Exception as E:
                self.con.rollback()
                return E
            
            finally:
                # Close the database connection
                self.cursor.close()
                self.con.close()    


    def delete_info(self, student_id):
            # connect to the database
            self.connect_dp()
            
            sql = f"DELETE FROM student_info WHERE studentId = '{student_id}'"

            try:
                # Execute the sql query for deleting info
                self.cursor.execute(sql)
                print(f"delete result = {sql}")
                self.con.commit()
            except Exception as E:
                self.con.rollback()
                return E
            
            finally:
                # Close the database connection
                self.cursor.close()
                self.con.close()    

    def search_info(self,student_id=None,first_name=None,last_name=None,state=None,email_address=None,city=None):
            self.connect_dp()

            condition = ""
            if student_id:
                condition+= f"studentId LIKE '%{student_id}%'"
            else:
                if first_name:
                    if condition:
                        condition+= f" and firstName LIKE '%{first_name}%'"
                    else:
                        condition+= f"firstName LIKE '%{first_name}%'"
                if last_name:
                    if condition:
                        condition+= f" and lastName LIKE '%{last_name}%'"
                    else:
                        condition+= f"lastName LIKE '%{last_name}%'"
                if state:
                    if condition:
                        condition+= f" and state LIKE '%{state}%'"
                    else:
                        condition+= f"state LIKE '%{state}%'"
                if city:
                    if condition:
                        condition+= f" and city LIKE '%{city}%'"
                    else:
                        condition+= f"city LIKE '%{city}%'"
                if email_address:
                    if condition:
                        condition+= f" and emailAddress LIKE '%{email_address}%'"
                    else:
                        condition+= f"emailAddress LIKE '%{email_address}%'"
            if condition:
                sql = f"""
                SELECT * FROM student_info WHERE {condition};
                """
            else:
                sql = "SELECT * FROM student_info;"

            try:
                # Execute the sql query for searching info
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            except Exception as E:
                return E
            
            finally:
                # Close the database connection
                self.cursor.close()
                self.con.close()
       
    def get_all_states(self):
            self.connect_dp()

            sql = f"""
            SELECT state FROM student_info GROUP BY state;
            """

            try:
                # Execute the sql query for getting all states
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                return result
            except Exception as E:
                return E
            
            finally:
                # Close the database connection
                self.cursor.close()
                self.con.close()        


    def get_data_from_database(self):
        try:
            self.cursor.execute("SELECT studentId,firstName,lastName,emailAddress,state,city FROM student_info")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.cursor.close()            

    def get_all_cities(self):
            self.connect_dp() 

            sql = f"""
            SELECT city FROM student_info GROUP BY city;
            """

            try:
                # Execute the sql query for getting all cities
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                return result
            except Exception as E:
                self.con.rollback()
                return E
            
            finally:
                # Close the database connection
                self.cursor.close()
                self.con.close()    