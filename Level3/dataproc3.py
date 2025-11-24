from processor3 import Myprocessor
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    dp=Myprocessor(args.input)
    dp.show_data()
    
if __name__ == '__main__':
    main()
