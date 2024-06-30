import streamlit as st
from components import input_reader,dashboard

def home() -> None:
    st.title("Welcome to SpendWise")
    df = input_reader.input_reader()

    if df:
        dash = dashboard.dashboard(df)
        st.title("Your Data")

        dash.display_all()



if __name__ == '__main__':
    home()