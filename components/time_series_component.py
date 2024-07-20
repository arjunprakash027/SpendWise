import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

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
        self.df_ts = pd.DataFrame()

    def _calculate_time_series(self) -> None:
        if self.df.check_columns(["Date","Amount"]):
            self.df_main['Date'] = pd.to_datetime(pd.to_datetime(self.df_main['Date'], format='%d/%m/%Y %H:%M:%S').dt.date)
            self.df_ts = self.df_main[['Date','Amount']]

            self.df_ts.set_index('Date', inplace=True)

            daily_expenses = self.df_ts.resample('D').sum()
            daily_expenses.index = pd.to_datetime(daily_expenses.index)

            adfuller_result = adfuller(daily_expenses.dropna())

            if adfuller_result[1] > 0.05:
                daily_expenses = daily_expenses.diff().dropna()

            sarima_model = SARIMAX(daily_expenses, order=(1, 1, 1), seasonal_order=(1, 1, 1, 30))
            sarima_result = sarima_model.fit(disp=False)

            days_in_future:int = st.slider("Predict for number of days in future", 0, 60, 25)


            forecast = sarima_result.get_forecast(steps=days_in_future)
            forecast_df = forecast.predicted_mean
            conf_int = forecast.conf_int()

            plt.figure(figsize=(10, 6))
            plt.plot(daily_expenses, label='Daily Expenses')
            plt.plot(forecast_df, label='Forecast', color='red')
            plt.fill_between(conf_int.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3)
            plt.title('Expense Forecast')
            plt.xlabel('Date')
            plt.ylabel('Expense (INR)')
            plt.legend()

            st.pyplot(plt)


        else:
            st.write("Date column not present in the data sheet, Please include it to get this analytics")


    def display_all(self) -> None:
        self._calculate_time_series()