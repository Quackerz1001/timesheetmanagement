import hashlib
import streamlit as st
from databasehandler import DatabaseHandler

# Initialize the database handler
db_handler = DatabaseHandler('timesheetmanagement.db')

# Function to authenticate user
def authenticate(username, password):
    user = db_handler.read_user_by_username(username)
    if user and user[2] == hashlib.sha256(password.encode()).hexdigest():  # Check if password matches
        return True
    return False

@st.dialog("User Deletion")
def confirmUser(userID):
    st.write(f"Confirm deletion of user with ID: {userID}?")
    if st.button("Confirm"):
        db_handler.delete_user(userID)
        st.success("User deleted.")

@st.dialog("Timesheet Deletion")
def confirmTimesheet(timesheetID):
    st.write(f"Confirm deletion of timesheet with ID: {timesheetID}?")
    if st.button("Confirm"):
        db_handler.delete_timesheet(timesheetID)
        st.success("Timesheet deleted.")

@st.dialog("Logout")
def confirmLogout():
    st.write(f"Confirm logout?")
    if st.button("Confirm"):
        st.session_state.logged_in = False
        st.success("You have been logged out.")
        st.rerun()

def show_admin_app():
    # User management section
    st.header("User Management")

    # Read dataframe from the database
    df = db_handler.read_users_dataframe()
    st.dataframe(df, hide_index = True)

    # Create User
    st.subheader("Create User")
    new_username = st.text_input("New Username",key="nu1")
    new_password = st.text_input("New Password", type="password",key="np1")
    if st.button("Create User"):
        user_create = db_handler.read_user_by_username(new_username)
        if not user_create:
            user_id = db_handler.create_user(new_username, hashlib.sha256(new_password.encode()).hexdigest(), False)
            st.success(f"User created with ID: {user_id}")
        else:
            st.error("User with that username already exists.")

    # Read User
    st.subheader("Read User")
    username_to_read = st.text_input("Username")
    if st.button("Fetch User"):
        user = db_handler.read_user_by_username(username_to_read)
        if user:
            st.write(f"User ID: {user[0]}, Username: {user[1]}")
        else:
            st.error("User not found.")

    # Update User
    st.subheader("Update User")
    user_id_to_update = st.number_input("User ID to Update", min_value=1)
    new_username = st.text_input("New Username",key="nu2")
    new_password = st.text_input("New Password", type="password",key="np2")
    if st.button("Update User"):
        user_update = db_handler.read_user(user_id_to_update)
        user_update_check = db_handler.read_user_by_username(new_username)
        if user_update:
            if not user_update_check or user_update_check[0] == user_update[0]:
                db_handler.update_user(user_id_to_update, new_username, hashlib.sha256(new_password.encode()).hexdigest())
                st.success("User updated.")
            else:
                st.error("Username already in use.")
        else:
            st.error("User does not exist.")
        

    # Delete User
    st.subheader("Delete User")
    user_id_to_delete = st.number_input("User ID to Delete", min_value=1)
    if st.button("Delete User"):
        confirmUser(user_id_to_delete)

    # Logout option
    if st.button("Logout"):
        confirmLogout()


def show_main_app():
    # Timesheet management section
    st.header("Timesheet Management")

    # Read dataframe from the database
    df = db_handler.read_timesheets_dataframe(st.session_state.userID)
    st.dataframe(df, hide_index = True)

    # Create Timesheet
    st.subheader("Create Timesheet")
    project_name = st.text_input("Project Name")
    hours_spent = st.number_input("Hours Spent", min_value=1, max_value=8)
    date = st.date_input("Date")
    if st.button("Create Timesheet"):
        timesheet_create = db_handler.read_timesheet_by_date(st.session_state.userID, date)
        if not project_name == "":
            if not timesheet_create:
                timesheet_id = db_handler.create_timesheet(st.session_state.userID, project_name, hours_spent, date)
                st.success(f"Timesheet created with ID: {timesheet_id}")
            else:
                st.error("Timesheet exists for date.")
        else:
            st.error("Project name cannot be blank.")

    # Read Timesheet
    st.subheader("Read Timesheet")
    timesheet_date_to_read = st.date_input("Timesheet Date")
    if st.button("Fetch Timesheet"):
        timesheet_read = db_handler.read_timesheet_by_date(st.session_state.userID, timesheet_date_to_read)
        if timesheet_read:
                st.write(f"Timesheet ID: {timesheet_read[0]}, User ID: {timesheet_read[1]}, Project Name: {timesheet_read[2]}, Hours Spent: {timesheet_read[3]}, Date: {timesheet_read[4]}")
        else:
            st.error("Timesheet not found.")

    # Update Timesheet
    st.subheader("Update Timesheet")
    timesheet_id_to_update = st.number_input("Timesheet ID to Update", min_value=1)
    new_project_name = st.text_input("New Project Name")
    new_hours_spent = st.number_input("New Hours Spent", min_value=1, max_value=8)
    new_date = st.date_input("New Date")
    if st.button("Update Timesheet"):
        timesheet_update = db_handler.read_timesheet(timesheet_id_to_update)
        timesheet_update_date = db_handler.read_timesheet_by_date(st.session_state.userID, new_date)
        if timesheet_update:
            if timesheet_update[1] == st.session_state.userID:
                if not timesheet_update_date or timesheet_update_date[0] == timesheet_id_to_update:
                    db_handler.update_timesheet(timesheet_id_to_update, st.session_state.userID, new_project_name, new_hours_spent, new_date)
                    st.success("Timesheet updated.")
                else:
                    st.error("Timesheet exists for date.")
            else:
                st.error("Timesheet not owned by user.")
        else:
            st.error("Timesheet not found.")

    # Logout option
    if st.button("Logout"):
        confirmLogout()
        

def show_main_app_admin():
    # Timesheet management section
    st.header("Timesheet Management")

    # Read dataframe from the database
    df = db_handler.read_timesheets_admin_dataframe()
    st.dataframe(df, hide_index = True)

    # Create Timesheet
    st.subheader("Create Timesheet")
    user_id_for_timesheet = st.number_input("User ID for Timesheet", min_value=1)
    project_name = st.text_input("Project Name")
    hours_spent = st.number_input("Hours Spent", min_value=1, max_value=8)
    date = st.date_input("Date")
    if st.button("Create Timesheet"):
        timesheet_user_create = db_handler.read_user(user_id_for_timesheet)
        timesheet_create = db_handler.read_timesheet_by_date(user_id_for_timesheet, date)
        if timesheet_user_create:
            if not timesheet_create:
                timesheet_id = db_handler.create_timesheet(user_id_for_timesheet, project_name, hours_spent, date)
                st.success(f"Timesheet created with ID: {timesheet_id}")
            else:
                st.error(f"Timesheet exists for date and user. Timesheet ID: {timesheet_create[0]}")
        else:
            st.error(f"User does not exist.")
        

    # Read Timesheet
    st.subheader("Read Timesheet")
    timesheet_id_to_read = st.number_input("Timesheet ID", min_value=1)
    if st.button("Fetch Timesheet"):
        timesheet_read = db_handler.read_timesheet(timesheet_id_to_read)
        if timesheet_read:
            st.write(f"Timesheet ID: {timesheet_read[0]}, User ID: {timesheet_read[1]}, Project Name: {timesheet_read[2]}, Hours Spent: {timesheet_read[3]}, Date: {timesheet_read[4]}")
        else:
            st.error("Timesheet not found.")

    # Update Timesheet
    st.subheader("Update Timesheet")
    timesheet_id_to_update = st.number_input("Timesheet ID to Update", min_value=1)
    new_project_name = st.text_input("New Project Name")
    new_hours_spent = st.number_input("New Hours Spent", min_value=1, max_value=8)
    new_date = st.date_input("New Date")
    if st.button("Update Timesheet"):
        timesheet_update = db_handler.read_timesheet(timesheet_id_to_update)
        if timesheet_update:
            timesheet_update_date = db_handler.read_timesheet_by_date(timesheet_update[1], new_date)
            if not timesheet_update_date or timesheet_update_date[0] == timesheet_id_to_update:
                db_handler.update_timesheet(timesheet_id_to_update, timesheet_update[1], new_project_name, new_hours_spent, new_date)
                st.success("Timesheet updated.")
            else:
                st.error(f"Timesheet exists for date and user. Timesheet ID: {timesheet_update_date[0]}")
        else:
            st.error("Timesheet not found.")
        

    # Delete Timesheet
    st.subheader("Delete Timesheet")
    timesheet_id_to_delete = st.number_input("Timesheet ID to Delete", min_value=1)
    if st.button("Delete Timesheet"):
        timesheet_delete = db_handler.read_timesheet(timesheet_id_to_delete)
        if timesheet_delete:
            confirmTimesheet(timesheet_id_to_delete)
        else:
            st.error(f"Timesheet does not exist.")
        

    # Logout option
    if st.button("Logout"):
        confirmLogout()


def login_page():
    if db_handler.adminRequired == True:
        st.subheader("Create Admin")
        admin_username = st.text_input("New Username",key="nu1")
        admin_password = st.text_input("New Password", type="password",key="np1")
        if st.button("Create User"):
            user_id = db_handler.create_user(admin_username, hashlib.sha256(admin_password.encode()).hexdigest(), True)
            st.success(f"User created with ID: {user_id}")
            db_handler.adminRequired = False
            st.rerun()
    else:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.success("Login successful!")
                user = db_handler.read_user_by_username(username)
                if user[3]:
                    st.session_state.userID = user[0]
                    st.session_state.logged_in = "admin"
                else:
                    st.session_state.userID = user[0]
                    st.session_state.logged_in = "user"
                st.rerun()
                
            else:
                st.error("Invalid username or password.")
        