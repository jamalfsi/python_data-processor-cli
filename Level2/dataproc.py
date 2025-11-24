from processor import DataProcessor
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    dp = DataProcessor(args.input)
    dp.show_info()

# from processor import DataProcessor  # Import the class from processor.py

# def main():
#     # Example: hardcoded filename and action
#     filename = 'sample_sales.csv'
#     dp = DataProcessor(filename)
#     dp.show_info()

if __name__ == '__main__':
    main()
