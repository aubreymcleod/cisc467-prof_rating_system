"""
This framework defines a system for running multiple apps off a single Streamlit instance.
Credit: giswqs - https://github.com/giswqs/geemap-apps from the Streamlit Example library
"""
import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """
        Add a new application to the website
        :param title: the label used in the navigation bar.
        :param func: the python function that renders the application
        """
        self.apps.append({"title": title, "function": func})

    def run(self):
        app_state = st.experimental_get_query_params()
        app_state = {
            k: v[0] if isinstance(v, list) else v for k, v in app_state.items()
        } # get the first item in each query string

        titles = [a["title"] for a in self.apps]
        functions = [a["function"] for a in self.apps]
        default_radio = titles.index(app_state["page"]) if "page" in app_state else 0

        st.sidebar.title("Navigation")

        title = st.sidebar.radio("Go To", titles, index=default_radio, key="radio")

        app_state["page"] = st.session_state.radio

        st.experimental_set_query_params(**st.session_state.to_dict())
        functions[titles.index(title)]()
