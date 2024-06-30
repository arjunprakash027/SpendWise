import streamlit as st
import pandas as pd

from pathlib import Path
import sys
current_script = Path(__file__).resolve()
parent_directory = current_script.parent.parent
sys.path.append(str(parent_directory))

from utils.csv_xls_reader import CSVXLSData

class dashboard:

    def __init__(self,df:CSVXLSData) -> None:
        self.df = df
        
    def display_table(self) -> None:
        col1,col2 = st.columns(2)
        col1.metric(label="No. of Rows", value=len(self.df))
        col2.metric(label="No. of Columns", value=len(self.df.columns()))
        st.dataframe(self.df.data)