import enum

from database_tools import *

# Enumeration representing program states
class State(enum.Enum):
    START = 0
    ADD_USER = 1
    LOGIN = 2
    DASHBOARD = 3
    PLATFORM = 4
    ADD_PLATFORM = 5
    END = 6

# Class representing a state machine to control program flow
class State_Machine:
    # Constructor
    def __init__(self):
        # Fields
        self.state = State.START                                # Program state
        self.user_name = ""                                     # User's name if logged in
        self.user_date_created = ""                             # User creation date if logged in
        self.platforms = []                                     # User's platforms if logged in
        self.current_platform = -1                              # Platform to be viewed/modified
        self.db_connection = connect_to_db(DB_RELATIVE_PATH)    # Database connection
        self.db_cursor = self.db_connection.cursor()            # Database cursor

        create_db(self.db_connection, self.db_cursor)       # Creates DB if none is found.
        #populate_db(self.db_connection, self.db_cursor)     # Uncomment on first use to populate DB.

    # Method to run the state machine
    # Only appropriate method to call from outside class.
    # All others are internal (no private in Python).
    def run(self):
        while (True):
            match self.state:
                case State.START:
                    self.start()
                case State.ADD_USER:
                    self.add_user()
                case State.LOGIN:
                    self.login()
                case State.DASHBOARD:
                    self.dashboard()
                case State.PLATFORM:
                    self.platform()
                case State.ADD_PLATFORM:
                    self.add_platform()
                case State.END:
                    self.end()
                    break
    
    # Start state method
    # Lets user proceed to new user, login, or end states.
    def start(self):
        print("PASSWORD MANAGER PROTOTYPE")
        self.state = self.start_get_next_state()
        print()
    
    # Start state support method
    # Gets next state selection from user.
    def start_get_next_state(self):
        while (True):
            command = input("Enter command (add, login, end):\t")

            match command.lower():
                case "add":
                    return State.ADD_USER
                case "login":
                    return State.LOGIN
                case "end":
                    return State.END
                case _:
                    print("Invalid command.")

    # Add user state method
    # Lets user attempt to add a username and password and returns to start state.
    def add_user(self):
        print("ADD USER")

        new_username = input("Enter new username:\t")

        if (self.username_available(new_username)):
            new_password_1 = input("Enter new password:\t")
            new_password_2 = input("Verify new password:\t")

            if (State_Machine.passwords_valid(new_password_1, new_password_2)):
                salt = random_string(SALT_LENGTH)
                new_password = salted_hash(new_password_1, salt)

                self.db_cursor.execute("INSERT INTO user (name, password, salt, locked, date_added) "
                                        + "VALUES (?, ?, ?, FALSE, date(date(), 'localtime'));",
                                        [new_username, new_password, salt])
                self.db_connection.commit()
                print("User added.")
            else:
                print("Invalid password.")
        else:
            print("Invalid username.")

        self.state = State.START

        print()
    
    # Determines if given proposed username is valid and available.
    def username_available(self, username):
        if (len(username) >= USER_USERNAME_MIN_LENGTH):
            self.db_cursor.execute("SELECT name "
                                   + "FROM user "
                                   + "WHERE name=?;",
                                   [username])

            name_rows = self.db_cursor.fetchall()

            if (len(name_rows) == 0):
                return True
            else:
                return False
        else:
            return False
    
    # Static
    # Determines if given proposed user passwords are equal and valid.
    def passwords_valid(password_1, password_2):
        if (password_1 == password_2 and len(password_1) >= USER_PASSWORD_MIN_LENGTH):
            return True
        else:
            return False

    # Login state method
    # Lets user attempt to log into an account.
    # Retrieves user info and proceeds to dashboard state on success or returns to start state on failure.
    def login(self):
        print("LOGIN")

        username = input("Enter username:\t")
        password = input("Enter password:\t")

        if (self.validate_credentials(username, password)):
                self.state = State.DASHBOARD
        else:
            State_Machine.print_login_error()

            self.state = State.START
        
        print()
    
    # Determines if given credentials are valid and sets fields if so.
    def validate_credentials(self, username, password):
        self.db_cursor.execute("SELECT salt "
                               + "FROM user "
                               + "WHERE name=? AND locked=FALSE;",
                               [username])

        salt_rows = self.db_cursor.fetchall()

        if (len(salt_rows) > 0):
            salt = salt_rows[0][0]
            password = salted_hash(password, salt)

            self.db_cursor.execute("SELECT name, date_added "
                                   + "FROM user "
                                   + "WHERE name=? AND password=? AND locked=FALSE;",
                                   [username, password])

            user_rows = self.db_cursor.fetchall()

            if (len(user_rows) > 0):
                self.user_name = user_rows[0][0]
                self.user_date_created = user_rows[0][1]

                self.update_platforms()

                return True
            else:
                return False
        else:
            return False
    
    # Updates platforms field.
    def update_platforms(self):
        self.db_cursor.execute("SELECT number, name, location, date_added "
                               + "FROM platform "
                               + "WHERE for_user=?;", [self.user_name])
        
        self.platforms = self.db_cursor.fetchall()
        
    # Static
    # Prints a generic error message for failed login.
    def print_login_error():
        print("Login credentials are invalid, or account is locked.")

    # Dashboard state method
    # Displays user info and platforms.
    # Allows user to reveal a platform password or proceed to add platform, platform detail, or end states.
    def dashboard(self):
        print("DASHBOARD")
        print("Welcome, " + self.user_name + "!")
        print("Date joined:\t" + self.user_date_created)
        State_Machine.print_rows(self.platforms)

        self.state = self.dashboard_get_next_state()

        print()

    # Static
    # Prints all columns of all given rows in order.
    def print_rows(rows):
        for i in rows:
            for j in i:
                print(j)

    # Dashboard state support method
    # Gets next state selection from user.
    def dashboard_get_next_state(self):
        while (True):
            command = input("Enter command (addpf, pass, detail, end):\t")

            match command.lower():
                case "addpf":
                    return State.ADD_PLATFORM
                case "pass":
                    if (self.update_current_platform()):
                        self.db_cursor.execute("SELECT value, date_added "
                                               + "FROM password "
                                               + "WHERE for_user=? AND for_platform=? "
                                               + "AND date_added=(SELECT max(date_added) "
                                                                  + "FROM password "
                                                                  + "WHERE for_user=? AND for_platform=?);",
                                               [self.user_name, self.current_platform, self.user_name, self.current_platform])
                        
                        password_row = self.db_cursor.fetchall()
                        
                        if (len(password_row) > 0):
                            print(password_row[0][0])
                            print(password_row[0][1])
                        else:
                            print("Platform has no password.")
                    else:
                        print("Invalid platform number.")
                case "detail":
                    if (self.update_current_platform()):
                        return State.PLATFORM
                    else:
                        print("Invalid platform number.")
                case "end":
                    return State.END
                case _:
                    print("Invalid command.")
    
    # Gets platform number from user, determines if it is valid, and updates current_platform field if so.
    def update_current_platform(self):
        platform_number = input("Enter platform number:\t")

        for i in self.platforms:
            if (str(i[0]) == platform_number):
                self.current_platform = platform_number

                return True
            
        return False
    
    # Platform state method
    def platform(self):
        print("PLATFORM")
        # print name, date added, location
        # print password history in order
        # commands: addpw, genpw, delete, back, end
            # addpw - add valid user-generated password
            # genpw - auto-generate new password
            # delete - delete platform and associated passwords
            # back - to dashboard
            # end - end program
        self.state = State.DASHBOARD
        
        print()

    # Add platform state method
    # Lets user attempt to add a new platform.
    # Proceeds to platform state if successful, or returns to dashboard if not.
    def add_platform(self):
        print("ADD PLATFORM")

        platform_name = input("Enter platform name:\t")

        if (self.platform_name_valid(platform_name)):
            platform_location = input("Enter platform URL or filepath:\t")

            self.db_cursor.execute("INSERT INTO platform (name, location, date_added, for_user) "
                                   + "VALUES (?, ?, date(date(), 'localtime'), ?);",
                                   [platform_name, platform_location, self.user_name])
            self.db_connection.commit()
            self.update_platforms()
            print("Platform added.")

            self.state = State.PLATFORM
        else:
            print("Invalid platform name.")

            self.state = State.DASHBOARD
        
        print()

    # Determine if given proposed platform name is valid.
    def platform_name_valid(self, platform_name):
        if (len(platform_name) == 0):
            return False
        else:
            for i in self.platforms:
                if (str(i[1]) == platform_name):
                    return False
            
        return True

    # End state method
    # Performs cleanup and output before program close.
    def end(self):
        print("END")
        print("Ending program . . .")

        self.user_name = ""
        self.date_created = ""
        self.platforms = []
        self.current_platform = -1

        self.db_connection.close()
        print()