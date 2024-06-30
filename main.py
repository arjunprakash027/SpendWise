import streamlit as st
from apps.input_reader import input_reader

def home() -> None:
    st.title("Welcome to Spend Analyser")
    input_reader()

if __name__ == '__main__':
    home()