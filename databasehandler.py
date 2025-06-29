import sqlite3
from sqlite3 import Error
import pandas as pd

class DatabaseHandler:
    def __init__(self, db_file):
        """Initialize the database file."""
        self.db_file = db_file
        self.adminRequired = False
        self.initialize_db()

    def create_connection(self):
        """Create a database connection to the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def initialize_db(self):
        """Initialize the database and create an admin user if the users table is empty."""
        self.create_tables()
        if self.read_user_count() == 0:
            self.adminRequired = True

    def create_tables(self):
        """Create the necessary tables in the database."""
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    is_admin BOOLEAN NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timesheets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    project_name TEXT NOT NULL,
                    hours_spent INTEGER NOT NULL,
                    date DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()

    def read_user_count(self):
        """Return the count of users in the users table."""
        with self.create_connection() as conn:
            sql = '''SELECT COUNT(*) FROM users'''
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchone()[0]

    def read_users_dataframe(self):
        with self.create_connection() as conn:    
            query = "SELECT id, username, is_admin FROM users"  # Adjust the query as needed
            df = pd.read_sql_query(query, conn)
            return df

    def read_timesheets_admin_dataframe(self):
        with self.create_connection() as conn:    
            query = "SELECT * FROM timesheets"  # Adjust the query as needed
            df = pd.read_sql_query(query, conn)
            return df

    def read_timesheets_dataframe(self, userID):
        with self.create_connection() as conn:    
            query = "SELECT * FROM timesheets WHERE user_id = ?"  # Adjust the query as needed
            df = pd.read_sql_query(query, conn, params=(userID,))
            return df

    def create_user(self, username, password, is_admin):
        """Create a new user in the users table."""
        with self.create_connection() as conn:
            sql = '''INSERT INTO users(username, password, is_admin) VALUES(?, ?, ?)'''
            cur = conn.cursor()
            cur.execute(sql, (username, password, is_admin))
            conn.commit()
            return cur.lastrowid

    def read_user(self, user_id):
        """Fetch a user by user_id."""
        with self.create_connection() as conn:
            sql = '''SELECT * FROM users WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            return cur.fetchone()

    def read_user_by_username(self, username):
        """Fetch a user by username."""
        with self.create_connection() as conn:
            sql = '''SELECT * FROM users WHERE username = ?'''
            cur = conn.cursor()
            cur.execute(sql, (username,))
            return cur.fetchone()

    def update_user(self, user_id, username, password):
        """Update a user's information."""
        with self.create_connection() as conn:
            sql = '''UPDATE users SET username = ?, password = ? WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, (username, password, user_id))
            conn.commit()

    def delete_user(self, user_id):
        """Delete a user by user_id."""
        with self.create_connection() as conn:
            sql = '''DELETE FROM users WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            conn.commit()

    def create_timesheet(self, user_id, project_name, hours_spent, date):
        """Create a new timesheet entry."""
        with self.create_connection() as conn:
            sql = '''INSERT INTO timesheets(user_id, project_name, hours_spent, date) VALUES(?, ?, ?, ?)'''
            cur = conn.cursor()
            cur.execute(sql, (user_id, project_name, hours_spent, date))
            conn.commit()
            return cur.lastrowid

    def read_timesheet(self, timesheet_id):
        """Fetch a timesheet by timesheet_id."""
        with self.create_connection() as conn:
            sql = '''SELECT * FROM timesheets WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, (timesheet_id,))
            return cur.fetchone()
        
    def read_timesheet_by_date(self, user_id, date):
        """Fetch a timesheet by timesheet_id."""
        with self.create_connection() as conn:
            sql = '''SELECT * FROM timesheets WHERE user_id = ? AND date = ?'''
            cur = conn.cursor()
            cur.execute(sql, (user_id, date))
            return cur.fetchone()

    def update_timesheet(self, timesheet_id, user_id, project_name, hours_spent, date):
        """Update a timesheet entry."""
        with self.create_connection() as conn:
            sql = '''UPDATE timesheets SET user_id = ?, project_name = ?, hours_spent = ?, date = ? WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, (user_id, project_name, hours_spent, date, timesheet_id))
            conn.commit()

    def delete_timesheet(self, timesheet_id):
        """Delete a timesheet by timesheet_id."""
        with self.create_connection() as conn:
            sql = '''DELETE FROM timesheets WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, (timesheet_id,))
            conn.commit()

    # def close_connection(self):
    #     """Close the database connection."""
    #     if self.connection:
    #         self.connection.close()

