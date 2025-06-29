import streamlit as st
import frontendhandler

# Start the Streamlit app
if __name__ == "__main__":
    
    st.set_page_config(page_title="Consulting Timesheet Management")
    # Streamlit app title
    st.title("Consulting Timesheet Management")

    # Login section
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        nav = st.navigation([frontendhandler.login_page], position="hidden")
        nav.run()
    else:
        if st.session_state.logged_in == "admin":
            nav = st.navigation([
                st.Page(frontendhandler.show_main_app_admin,title="Timesheets"),
                st.Page(frontendhandler.show_admin_app,title="User Management")
            ])
        else:
            nav = st.navigation([
                st.Page(frontendhandler.show_main_app,title="Timesheets")
            ])
        nav.run()
        # st.switch_page(frontendhandler.show_main_app)
