import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print("Starting...")
        result = func(*args, **kwargs)
        end = time.time()
        print("Done! That took", round(end - start, 2), "seconds.")
        return result
    return wrapper

@timer
def show_data(data):
    print(data.head())

# Usage
import pandas as pd
data = pd.read_csv('sample_sales.csv')
show_data(data)
