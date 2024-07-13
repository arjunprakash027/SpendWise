import streamlit as st
from components import input_reader,dashboard

def home() -> None:
    st.title("Welcome to SpendWise")
    df = input_reader.input_reader()

    if 'available' not in st.session_state:
        st.session_state['available'] = False

    if df:
        st.session_state['df'] = df
        st.session_state['available'] = True

    if st.session_state['available']:
        df = st.session_state['df']
        col1,col2 = st.columns(2)
        col1.metric(label="No. of Rows", value=len(df))
        col2.metric(label="No. of Columns", value=len(df.columns()))
        st.dataframe(df.data)

        st.write("check out this [link](/basic_analysis) for dashboard on your data!")

if __name__ == '__main__':
    home()