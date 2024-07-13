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
        self.df_main = self.df.data.copy(deep=False)
        self.df_show = self.df.data.copy(deep=False)

    def _change_date(self) -> None:
        if self.df.check_columns(["Date"]):

            self.df_main['Date'] = pd.to_datetime(pd.to_datetime(self.df_main['Date'], format='%d/%m/%Y %H:%M:%S').dt.date)
            self.df_show['Date'] = pd.to_datetime(pd.to_datetime(self.df_main['Date'], format='%d/%m/%Y %H:%M:%S').dt.date)


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
            st.write(self.df_show)
        else:
            st.write("Date column not present in the data sheet, Please include it to get this analytics")
        
    
    def _display_analytics(self) -> None:

        df = self.df_show
        grouped_by_day = df.groupby(df['Date'])['Amount'].sum().reset_index()

        if self.df.check_columns(["Date","Amount"]):
            
            if self.df.check_columns(["Category"]):
                unique_categories = self.df_show['Category'].unique()
                options = st.multiselect(
                "Choose single or multiple categories",
                unique_categories)
                if options:
                    df = self.df_show[self.df_show['Category'].isin(options)]

            oldest_date = self.df_show['Date'].min()
            latest_date = self.df_show['Date'].max() + timedelta(days=1)

            difference_in_date: timedelta = latest_date - oldest_date

            st.metric(label="Total",value=df['Amount'].sum())
            st.metric(label="Mean Spend",value=f"{df['Amount'].sum()/difference_in_date.days} per day")
            st.metric(label="Max Spent",value=df['Amount'].max())
            st.metric(label="Min Spent",value=df['Amount'].min())

            fig = px.line(grouped_by_day, x='Date', y='Amount', title='Amount Over Time',markers=True)

            st.plotly_chart(fig)

            if self.df.check_columns(["Category"]):
                group_category_data = self.df_show.groupby('Category')['Amount'].sum().reset_index()
                fig = px.pie(group_category_data, names='Category', values='Amount', title='Total Amount by Category')
                st.plotly_chart(fig)
        else:
            st.write("Date and Amount column not present in the data sheet, Please include it to get this analytics")


    def display_all(self) -> None:
        self._change_date()
        self._display_analytics() #displays analytics in tab