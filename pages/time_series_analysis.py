import streamlit as st
import pandas as pd
from typing import Dict
import plotly.express as px

from pathlib import Path
import sys
current_script = Path(__file__).resolve()
parent_directory = current_script.parent.parent
sys.path.append(str(parent_directory))
from components.time_series_component import timeseries

def time_series_page() -> None:

    if 'available' not in st.session_state:
        st.session_state['available'] = False
        
    st.header('Basic Analysis Page')
    if st.session_state['available']:
        ts_dash = timeseries(df=st.session_state['df'])
        ts_dash.display_all()
    else:
        st.write("provide the dataframe first!")
    
time_series_page()