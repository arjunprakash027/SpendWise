from dataclasses import dataclass,field
import pandas as pd
import streamlit as st
from typing import Any, List
from streamlit.runtime.uploaded_file_manager import UploadedFile


@dataclass
class CSVXLSData:
    file_path: UploadedFile
    data: pd.DataFrame = field(init=False)
    file_name:str = field(init=False)

    def __post_init__(self):
        self.file_name = self.file_path.name

        if self.file_name.endswith('xls'):
            self.data = pd.read_excel(self.file_path)
        elif self.file_name.endswith('csv'):
            self.data = pd.read_csv(self.file_path, encoding='utf-8')
        else:
            st.error("Uploaded file extension is not supported")
    
    def __len__(self) -> int:
        return self.data.shape[0]
    
    def __bool__(self):
        return bool(True)
    
    def columns(self) -> List:
        return _read_columns(self.data)
    
    def check_columns(self,columns:List) -> bool:

        return _required_columns(df=self.data,columns=columns)


def _read_columns(df:pd.DataFrame) -> List:
    
    #cleaning the dataframe
    # nothing yet!
    return list(df.columns)

def _required_columns(df:pd.DataFrame,columns:list) -> bool:

    column_list = _read_columns(df)
    # 1) check for neccessary columns in dataframe

    for column in columns:
        if column not in column_list:
            return False
    
    return True




    

