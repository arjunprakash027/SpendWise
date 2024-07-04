import streamlit as st
import pandas as pd
from datetime import datetime

from pathlib import Path
import sys
current_script = Path(__file__).resolve()
parent_directory = current_script.parent.parent
sys.path.append(str(parent_directory))

from utils.csv_xls_reader import CSVXLSData

def input_reader() -> CSVXLSData:
    spending_data = st.file_uploader(label="Choose your spending csv/xls",type=['csv','xls'])

    if spending_data is not None:
        file_extension = Path(spending_data.name).suffix
        
        if not file_extension.endswith(('.csv', '.xls')):
            st.write(f"{file_extension} is not allowed")
            return None

        
        spending_details = CSVXLSData(file_path=spending_data)

        return spending_details
