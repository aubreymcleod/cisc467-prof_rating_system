"""
This file defines a basic homepage that the user is first presented with; this contains a quick intro and dem
"""
import streamlit as st


def app():
    st.title("CISC 467 - Fuzzy Logic-based Professor Rating System")

    st.header("Introduction")
    st.markdown(
        """
        Lorem Ipsum sit dolet.
        """
    )
    st.header("Most Recently rated professor: ")
    st.write("[Put that here...]")

# background logic here