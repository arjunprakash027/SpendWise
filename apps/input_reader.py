import streamlit as st
import pandas as pd

from pathlib import Path
import sys
current_script = Path(__file__).resolve()
parent_directory = current_script.parent.parent
sys.path.append(str(parent_directory))

from utils.csv_reader import CSVData

def input_reader() -> None:
    spending_data = st.file_uploader("Choose your spending csv/xls")

    if spending_data is not None:
        file_extension = Path(spending_data.name).suffix
        
        if not file_extension.endswith(('.csv', '.xls')):
            raise Exception (f"{file_extension} is not allowed")
        else:
            spending_details = CSVData(file_path=spending_data)
            st.write(spending_details.file_path)
