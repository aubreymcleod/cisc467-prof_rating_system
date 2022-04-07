"""
This file defines an entry point for our multi-page Rate My Professor System.
"""
import sys

import streamlit as st
from streamlit import cli as stcli

from apps import display, home, rate
from multiapp import MultiApp

def main():
    st.set_page_config(layout="wide")

    apps = MultiApp()

    # pages for application
    apps.add_app("Homepage", home.app)
    apps.add_app("Lookup a Professor", display.app)
    apps.add_app("Rate a Professor", rate.app)

    # run the applications
    apps.run()

def __init__():
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())


if __name__ == "__main__":
    if not st._is_running_with_streamlit:
        __init__()
    else:
        main()