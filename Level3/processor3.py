import pandas as pd

class Myprocessor:
    def __init__(self,filename):
        self.filename = filename
        self.data = pd.read_csv(filename)

    def show_data(self):
        print("Shape",self.data.shape)
        print("Columns", list(self.data.columns))
        print(self.data.head())
 