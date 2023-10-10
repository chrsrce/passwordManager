# Database Tools

import os
import sqlite3

from password_tools import *

# "Constants"
# Use these instead of hard-coded literals for easier maintenance.
DB_RELATIVE_PATH = "db/prototype.db"

# Returns absolute path to given relative path, creating the path if it does not exist.
def absolute_path(relative_path):
    script_path = os.path.dirname(__file__)
    absolute_path = os.path.join(script_path, relative_path)

    os.makedirs(os.path.dirname(absolute_path), exist_ok = True)

    return absolute_path

# Connects to database at given relative path.
def connect_to_db(relative_path):
    return sqlite3.connect(absolute_path(relative_path))

# Creates a clean database if it does not already exist, using given connection and cursor.
def create_db(db_connection, db_cursor):
    db_cursor.execute("CREATE TABLE IF NOT EXISTS user ("
                      + "name TEXT PRIMARY KEY, "
                      + "password TEXT, "
                      + "salt TEXT, "
                      + "locked INTEGER, "
                      + "date_added INTEGER"
                      + ");")
    db_connection.commit()
    db_cursor.execute("CREATE TABLE IF NOT EXISTS platform ("
                      + "number INTEGER PRIMARY KEY, "
                      + "name TEXT, "
                      + "location TEXT, "
                      + "date_added INTEGER, "
                      + "for_user TEXT REFERENCES user(name) ON UPDATE CASCADE ON DELETE CASCADE"
                      + ");")
    db_connection.commit()
    db_cursor.execute("CREATE TABLE IF NOT EXISTS password ("
                      + "number INTEGER PRIMARY KEY, "
                      + "value TEXT, "
                      + "date_added INTEGER, "
                      + "for_user TEXT REFERENCES user(name) ON UPDATE CASCADE ON DELETE CASCADE, "
                      + "for_platform INTEGER REFERENCES platform(number) ON UPDATE CASCADE ON DELETE CASCADE"
                      + ");")
    db_connection.commit()

# Test function
# Populates the database with test values, using given connection and cursor.
def populate_db(db_connection, db_cursor):
    password = "doot"
    salt = random_string(SALT_LENGTH)
    password = salted_hash(password, salt)

    db_cursor.execute("INSERT INTO user (name, password, salt, locked, date_added) "
                      + "VALUES ('root', ?, ?, FALSE, date(date(), 'localtime'));", [password, salt])
    db_connection.commit()
    db_cursor.execute("INSERT INTO platform (name, location, date_added, for_user) "
                      + "VALUES ('Tax Program', 'C:\\stuff\\TaxProgram.exe', date(date(), 'localtime'), 'root');")
    db_connection.commit()
    db_cursor.execute("INSERT INTO platform (name, location, date_added, for_user) "
                      + "VALUES ('My Bank Account', 'bankybank.com', date(date(), 'localtime'), 'root');")
    db_connection.commit()
    db_cursor.execute("INSERT INTO platform (name, location, date_added, for_user) "
                      + "VALUES ('Video Games', 'vidyagames.com', date(date(), 'localtime'), 'root');")
    db_connection.commit()

    platform_password_1 = random_string(PLATFORM_PASSWORD_LENGTH)

    db_cursor.execute("INSERT INTO password (value, date_added, for_user, for_platform) "
                      + "VALUES (?, date(date(), 'localtime'), 'root', 1);", [platform_password_1])
    db_connection.commit()
    
    platform_password_2 = random_string(PLATFORM_PASSWORD_LENGTH)

    db_cursor.execute("INSERT INTO password (value, date_added, for_user, for_platform) "
                      + "VALUES (?, date(date(), 'localtime'), 'root', 2);", [platform_password_2])
    db_connection.commit()
    
    platform_password_3 = random_string(PLATFORM_PASSWORD_LENGTH)

    db_cursor.execute("INSERT INTO password (value, date_added, for_user, for_platform) "
                      + "VALUES (?, date(date(), 'localtime'), 'root', 3);", [platform_password_3])
    db_connection.commit()