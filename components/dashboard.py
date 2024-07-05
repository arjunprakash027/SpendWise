import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,timedelta

from pathlib import Path
import sys
current_script = Path(__file__).resolve()
parent_directory = current_script.parent.parent
sys.path.append(str(parent_directory))

from utils.csv_xls_reader import CSVXLSData

class dashboard:

    def __init__(self,df:CSVXLSData) -> None:
        self.start_date = 0
        self.end_date = 0
        self.df = df
        self.df_main = self.df.data
        self.df_show = self.df.data
        
    def _display_metric(self) -> None:
        col1,col2 = st.columns(2)
        col1.metric(label="No. of Rows", value=len(self.df))
        col2.metric(label="No. of Columns", value=len(self.df.columns()))

    def _change_date(self) -> None:
        if self.df.check_columns(["Date"]):

            self.df_main['Date'] = pd.to_datetime(self.df_main['Date'], format='%d/%m/%Y %H:%M:%S')
            self.df_show['Date'] = pd.to_datetime(self.df_main['Date'], format='%d/%m/%Y %H:%M:%S')

            oldest_date = self.df_main['Date'].min().strftime('%d/%m/%Y')
            latest_date = self.df_main['Date'].max().strftime('%d/%m/%Y')

            start_time,end_time = st.slider(
            "Select Range",
            min_value=datetime.strptime(oldest_date, '%d/%m/%Y'),
            max_value=datetime.strptime(latest_date, '%d/%m/%Y'),
            value=(datetime.strptime(oldest_date, '%d/%m/%Y'),datetime.strptime(latest_date, '%d/%m/%Y')),
            format="DD/MM/YY")

            time_filtered_df = self.df_main[(self.df_main['Date'] >= start_time) & (self.df_main['Date'] <= end_time + timedelta(days=1))]

            self.df_show = time_filtered_df
        else:
            st.write("Date column not present in the data sheet, Please include it to get this analytics")

    def _display_table(self) -> None:
        st.dataframe(self.df_show)
    
    def _display_analytics(self) -> None:
        tab1, tab2, tab3 = st.tabs(["Aggregation and Spend Tracker", "Category Breakdown", "Incomming analysis"])

        #tab 1
        if self.df.check_columns(["Date","Amount"]):
            # self.df_show['Date'] = pd.to_datetime(self.df_show['Date'], format='%d/%m/%Y %H:%M:%S')
            #self.df_show['Date'] = self.df_show['Date'].dt.date

            tab1.metric(label="Total",value=self.df_show['Amount'].sum())
            tab1.metric(label="Mean Spend",value=f"{round(self.df_show['Amount'].mean())} per day")
            tab1.metric(label="Max Spent",value=self.df_show['Amount'].max())
            tab1.metric(label="Min Spent",value=self.df_show['Amount'].min())
            # tab1.line_chart(self.df_show,x="Date",y="Amount")

            fig = px.line(self.df_show, x='Date', y='Amount', title='Amount Over Time',markers=True)

            tab1.plotly_chart(fig)
        else:
            tab1.write("Date and Amount column not present in the data sheet, Please include it to get this analytics")
        
        #category breakdown analysis
        if self.df.check_columns(["Category","Amount","Date"]):

            group_category_data = self.df_show.groupby('Category')['Amount'].sum().reset_index()
            fig = px.bar(group_category_data, x='Category', y='Amount', title='Total Amount by Category')
            tab2.plotly_chart(fig)

            #linechart based on unique categories
            unique_categories = self.df_show['Category'].unique()

            options = tab2.multiselect(
            "Choose single or multiple categories",
            unique_categories)
            
            if options:
                category_df = self.df_show[self.df_show['Category'].isin(options)]


                tab2.metric(label=f"Total",value=category_df['Amount'].sum())
                tab2.metric(label=f"Mean Spend",value=f"{round(category_df['Amount'].mean())} per day")
                tab2.metric(label=f"Max Spent",value=category_df['Amount'].max())
                tab2.metric(label=f"Min Spent",value=category_df['Amount'].min())
                # tab1.line_chart(self.df_show,x="Date",y="Amount")

                fig = px.line(category_df, x='Date', y='Amount', title='Amount Over Time',markers=True)

                tab2.plotly_chart(fig)
            else:
                tab2.write("Choose an category to show charts")

        else:
            tab2.write("Category, Amount and (or) Date column not present in the data sheet, Please include it to get this analytics")


    def display_all(self) -> None:
        self._change_date()
        with st.expander("View your Data"):
            self._display_metric() #displays the metrics
            self._display_table() #displays the table
        self._display_analytics() #displays analytics in tab