import time
import pandas as pd

# The same decorator, unchanged
def timer(func):
    def wrapper(*args, **kwargs):
        print("Starting")
        start = time.time()
        result = func(*args, **kwargs)
        print("Done in", round(time.time() - start, 2), "sec")
        return result
    return wrapper

class DataProcessor:   # We make a “recipe” for DataProcessor objects
    def __init__(self, filename):  # When we make a processor, we give it a file name
        self.filename = filename   # Save the filename for later
        self.data = None           # Start with no data

    @timer                    # Decorate the load method!
    def load(self):           # When we “load”, we read the file
        self.data = pd.read_csv(self.filename)
        print("Loaded", self.filename)

    @timer                    # Decorate the show method as well!
    def show(self):           # When we “show”, print first 5 lines of data
        print(self.data.head())

# Using the class
dp = DataProcessor('sample_sales.csv')  # Make a new DataProcessor object
dp.load()           # Loads the file, prints “Done in ... sec”
dp.show()           # Shows first 5 rows, also prints “Done in ... sec”
