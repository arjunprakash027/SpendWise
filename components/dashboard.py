import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
import sys
current_script = Path(__file__).resolve()
parent_directory = current_script.parent.parent
sys.path.append(str(parent_directory))

from utils.csv_xls_reader import CSVXLSData

class dashboard:

    def __init__(self,df:CSVXLSData) -> None:
        self.df = df
    
    def _display_metric(self) -> None:
        col1,col2 = st.columns(2)
        col1.metric(label="No. of Rows", value=len(self.df))
        col2.metric(label="No. of Columns", value=len(self.df.columns()))

    def _display_table(self) -> None:
        st.dataframe(self.df.data)
    
    def _display_analytics(self) -> None:
        tab1, tab2, tab3 = st.tabs(["Aggregation and Spend Tracker", "Incomming analysis", "Incomming analysis"])

        #tab 1
        if self.df.check_columns(["Date","Amount"]):
            self.df.data['Date'] = pd.to_datetime(self.df.data['Date'], format='%d/%m/%Y %H:%M:%S')
            #self.df.data['Date'] = self.df.data['Date'].dt.date

            tab1.metric(label="Total",value=self.df.data['Amount'].sum())
            tab1.metric(label="Mean Spend",value=f"{round(self.df.data['Amount'].mean())} per day")
            tab1.metric(label="Max Spent",value=self.df.data['Amount'].max())
            tab1.metric(label="Min Spent",value=self.df.data['Amount'].min())
            # tab1.line_chart(self.df.data,x="Date",y="Amount")

            fig = px.line(self.df.data, x='Date', y='Amount', title='Amount Over Time')

            tab1.plotly_chart(fig)
        else:
            tab1.write("Date and Amount column not present in the data sheet, Please include it to get this analytics")


    def display_all(self) -> None:
        with st.expander("View your Data"):
            self._display_metric() #displays the metrics
            self._display_table() #displays the table
        self._display_analytics() #displays analytics in tab