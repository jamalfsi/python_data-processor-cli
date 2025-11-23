import pandas as pd
import time

def timedecore(func):
    def wrapper(*args, **kwargs):        
        print("Starting time decoration")
        start=time.time()
        result = func(*args, **kwargs)
        end=time.time()
        print("It takes ",round(end - start,2),"seconds")
        return result
    return wrapper

@timedecore
def show_data():
    print("hi")

# def main():
show_data()

