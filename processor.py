import argparse
from processor import DataProcessor

def main():
    parser = argparse.ArgumentParser(description="Data Processor CLI")
    parser.add_argument('--input', required=True, help="Input/data file (CSV/Excel)")
    parser.add_argument('--clean', action='store_true', help="Clean data (remove nulls, duplicates)")
    parser.add_argument('--analyze', action='store_true', help="Analyze data (summary statistics)")
    parser.add_argument('--output', help="Output file for report (JSON/CSV)")
    args = parser.parse_args()

    dp = DataProcessor(args.input)
    if args.clean:
        dp.clean()
    if args.analyze:
        report = dp.analyze()
        if args.output:
            dp.save_report(report, args.output)
        else:
            print(report)

if __name__ == '__main__':
    main()
