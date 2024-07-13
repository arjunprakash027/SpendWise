import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,timedelta
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly


from pathlib import Path
import sys
current_script = Path(__file__).resolve()
parent_directory = current_script.parent.parent
sys.path.append(str(parent_directory))

from utils.csv_xls_reader import CSVXLSData

class timeseries:

    def __init__(self,df:CSVXLSData) -> None:
        self.df = df
        self.df_main = self.df.data.copy(deep=False)
        self.df_prophet = pd.DataFrame()

    def _calculate_time_series(self) -> None:
        if self.df.check_columns(["Date"]):
            self.df_prophet['ds'] = pd.to_datetime(pd.to_datetime(self.df_main['Date'], format='%d/%m/%Y %H:%M:%S').dt.date)
            self.df_prophet['y']  = self.df_main['Amount']

            m = Prophet()
            m.fit(self.df_prophet)

            days_in_future:int = st.slider("Predict for number of days in future", 0, 60, 25)

            future = m.make_future_dataframe(periods=days_in_future)

            forecast = m.predict(future)

            plot_plotly(m,forecast)

            fig = px.line(forecast, x='ds', y='yhat', title='Trend Over Time',markers=True)
            st.plotly_chart(fig)

            st.write(forecast)
        else:
            st.write("Date column not present in the data sheet, Please include it to get this analytics")


    def display_all(self) -> None:
        self._calculate_time_series()