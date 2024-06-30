from dataclasses import dataclass,field
import pandas as pd

@dataclass
class CSVData:
    file_path: str
    data: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.data = pd.read_excel(self.file_path)

    

