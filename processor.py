import argparse
from processor import DataProcessor

def main():
    """
    Main CLI entry point.
    
    Line-by-line:
    - Create ArgumentParser with description
    - Add arguments for each feature
    - Parse command-line arguments
    - Create DataProcessor instance
    - Execute requested operations based on flags
    """
    parser = argparse.ArgumentParser(
        description="Data Processor CLI - Clean, Analyze, and Visualize Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dataproc.py --input data.csv --clean --analyze --output report.json
  python dataproc.py --input data.csv --filter Sales > 500 --groupby Region
  python dataproc.py --input data.csv --plot Date Sales --kind line
        """
    )
    
    # Input/Output arguments
    parser.add_argument('--input', required=True, help="Input data file (CSV/Excel/JSON)")
    parser.add_argument('--output', help="Output file for report (JSON/CSV)")
    
    # Processing operations
    parser.add_argument('--clean', action='store_true', help="Clean data (remove duplicates/nulls)")
    parser.add_argument('--analyze', action='store_true', help="Analyze and generate statistics")
    parser.add_argument('--info', action='store_true', help="Show data overview")
    
    # Advanced features
    parser.add_argument('--filter', nargs=3, metavar=('COLUMN', 'OPERATOR', 'VALUE'),
                        help="Filter data: column operator value (e.g., Sales > 500)")
    parser.add_argument('--groupby', nargs=2, metavar=('COLUMN', 'FUNCTION'),
                        help="Group by column with aggregation (mean/sum/count/min/max)")
    parser.add_argument('--plot', nargs=2, metavar=('X_COL', 'Y_COL'),
                        help="Create plot with X and Y columns")
    parser.add_argument('--kind', default='line', 
                        choices=['line', 'bar', 'scatter', 'hist'],
                        help="Plot type (default: line)")
    
    args = parser.parse_args()
    
    # Create processor instance
    dp = DataProcessor(args.input)
    dp.show_info()
    
    # Execute operations in logical order
    if args.info:
        dp.show_info()
    
    if args.clean:
        dp.clean()
    
    if args.filter:
        col, op, val = args.filter
        # Try to convert value to number if possible
        try:
            val = float(val)
        except ValueError:
            pass  # Keep as string
        dp.filter_data(col, op, val)
    
    if args.groupby:
        col, func = args.groupby
        dp.group_by(col, func)
    
    if args.analyze:
        report = dp.analyze()
        if args.output:
            dp.save_report(report, args.output)
        else:
            print("\n📊 ANALYSIS REPORT:")
            import json
            print(json.dumps(report, indent=2, default=str))
    
    if args.plot:
        x_col, y_col = args.plot
        dp.plot_graph(x_col, y_col, args.kind)

if __name__ == '__main__':
    main()
