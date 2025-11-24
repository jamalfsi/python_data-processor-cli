import pandas as pd

class DataProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.data = pd.read_csv(filename)

    def show_info(self):
        print("Shape:", self.data.shape)
        print("Columns:", list(self.data.columns))
        print(self.data.head())
